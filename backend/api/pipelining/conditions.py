from pathlib import Path
from shutil import copytree
from typing import List

from pydicom import dcmread

from api import worker_session
from api.models.dicom import DicomNode
from api.models.pipeline import Pipeline, PipelineNodeStorageBucket, PipelineNodeStorageBucketItem, \
    PipelineNodeCondition, PipelineNode
from api.services import DatabaseService


class PipelineConditionManager(DatabaseService):
    _bucket: PipelineNodeStorageBucket = None
    _bucket_items: dict = None
    _starting_node: PipelineNode = None
    _conditions: List[PipelineNodeCondition] = None

    def __init__(self, pipeline: Pipeline, initiator: DicomNode, db):
        super().__init__()

        self.pipeline: Pipeline = pipeline
        self.initiator = initiator
        self._db = db

    @property
    def starting_node(self):
        if not self._starting_node:
            nodes = [n for n in self.pipeline.get_starting_nodes() if n.container_is_input]

            for node in nodes:
                if node.destination.is_rts:
                    self._starting_node = node
                elif DicomNode.compare(self.initiator, node.destination):
                    self._starting_node = node
                    break

        return self._starting_node

    @property
    def storage_bucket(self) -> PipelineNodeStorageBucket:
        if self._bucket:
            return self._bucket

        kwargs = {
            "dicom_node_id": self.initiator.id,
            "pipeline_node_id": self.starting_node.id
        }

        if bucket := PipelineNodeStorageBucket.query(self._db).filter_by(**kwargs).first():
            self._bucket = bucket
        else:
            self._bucket = PipelineNodeStorageBucket(**kwargs).save(db)

        return self._bucket

    @property
    def bucket_items(self):
        if not self._bucket_items:
            self._bucket_items = {item.tag: item for item in self.storage_bucket.items}

        return self._bucket_items

    def _update_bucket_item(self, tag, value):
        bucket_item = self.bucket_items.get(tag, PipelineNodeStorageBucketItem(
            pipeline_node_storage_bucket_id=self.storage_bucket.id,
            tag=tag,
            values=[]
        ))

        if value not in bucket_item.values:
            print(value)
            bucket_item.values.append(value)
            bucket_item.save(db)

    def has_conditions(self) -> bool:
        return bool(self.starting_node and self.starting_node.conditions)

    def add_series_to_storage_bucket(self, folder: Path):
        assert self.has_conditions()
        assert self.storage_bucket

        file = next(folder.iterdir())
        assert file.is_file()
        ds = dcmread(file)
        print(ds.SeriesInstanceUID)

        [self._update_bucket_item(c.tag, ds.get(c.tag)) for c in self.starting_node.conditions]

        copytree(folder, self._bucket.get_abs_path(), dirs_exist_ok=True)

    def check_conditions(self):
        q = self._db.query(PipelineNodeStorageBucketItem, PipelineNodeCondition)\
            .join(PipelineNodeStorageBucket)\
            .filter(
                PipelineNodeCondition.pipeline_node_id == self.starting_node.id,
                PipelineNodeStorageBucketItem.tag == PipelineNodeCondition.tag
            )

        for bucket_item, condition in q.all():
            expected = set(condition.values)
            have = set(bucket_item.values)

            if condition.match.lower() == 'all' and expected != have:
                return False
            elif condition.match.lower() == 'any' and expected.isdisjoint(have):
                return False

        return True


if __name__ == '__main__':
    with worker_session() as db:
        pipeline = Pipeline.query(db).first()
        node = DicomNode.query(db).first()

        mgr = PipelineConditionManager(pipeline, node, db)
        print(mgr.check_conditions())
