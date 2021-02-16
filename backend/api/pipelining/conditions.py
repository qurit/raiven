from typing import List
from pathlib import Path
from shutil import copytree

from api import config
from api.services import DatabaseService
from api.models.pipeline import Pipeline, PipelineStorageBucket, PipelineStorageBucketItem
from api.models.dicom import DicomNode

from api import worker_session


class PipelineConditionManager(DatabaseService):
    _bucket: PipelineStorageBucket = None

    def __init__(self, pipeline: Pipeline, initiator: DicomNode, db):
        super().__init__()

        self.pipeline: Pipeline = pipeline
        self.initiator = initiator
        self._db = db

    def _get_storage_bucket(self) -> PipelineStorageBucket:
        if self._bucket:
            return self._bucket

        q = PipelineStorageBucket.query(self._db)
        q = q.filter_by(dicom_node_id=self.initiator.id, pipeline_id=self.pipeline.id)
        if bucket := q.first():
            self._bucket = bucket
        else:
            self._bucket = PipelineStorageBucket(
                dicom_node_id=self.initiator.id,
                pipeline_id=self.pipeline.id
            ).save(db)

        return self._bucket

    def has_conditions(self) -> bool:
        nodes = [n for n in self.pipeline.get_starting_nodes() if n.container_is_input]

        starting_node = None
        for node in nodes:
            if node.destination.is_rts:
                starting_node = node
            elif DicomNode.compare(self.initiator, node.destination):
                starting_node = node
                break

        return bool(starting_node.conditions) if starting_node else False

    def add_to_storage_bucket(self, folder: Path):
        self._get_storage_bucket()
        copytree(folder, self._bucket.get_abs_path(), dirs_exist_ok=True)


if __name__ == '__main__':
    with worker_session() as db:
        pipeline = Pipeline.query(db).first()
        node = DicomNode.query(db).first()

        mgr = PipelineConditionManager(pipeline, node, db)
        if mgr.has_conditions():
            mgr.add_to_storage_bucket('.')