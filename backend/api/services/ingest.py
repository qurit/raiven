import pathlib
import shutil

from api import config
from api.models import utils
from api.models.dicom import DicomNode
from api.models.pipeline import Pipeline
from api.models.user import User
from api.pipelining import DicomIngestController, PipelineController
from api.services import DatabaseService, PipelineConditionService, DicomNodeService


class DicomIngestService(DatabaseService):
    class EmptyFolderException(Exception):
        pass

    def __init__(
        self,
        folder: pathlib.Path,
        called_aet: str,
        calling_aet: str,
        calling_host: str,
    ):
        super().__init__()

        self.folder = folder
        self.called_aet = called_aet
        self.calling_aet = calling_aet
        self.calling_host = calling_host
        self.initiator_node = None

    def __enter__(self):
        super().__enter__()

        self.initiator_node = DicomNodeService(self._db).get_from_connection(self.calling_aet, self.calling_host)
        assert self.initiator_node

        return self

    def execute(self):
        if not any(self.folder.iterdir()):
            shutil.rmtree(self.folder.resolve())

            # TODO: Better logging
            print("INFO: Empty ingested folder")
            raise self.EmptyFolderException('An Ingest Folder Cannot Be Empty')

        # Pushed to pipeline
        if self.called_aet.startswith(config.PIPELINE_AE_PREFIX):
            self._ingest_through_pipeline()

        # Pushed to user
        elif self.called_aet.startswith(config.USER_AE_PREFIX):
            self._ingest_to_user()

        # Pushed globally
        elif self.called_aet == config.SCP_AE_TITLE:
            self._ingest_globally()


        # Pushed to an undefined location
        else:
            print("ERROR: Undefined called AET")
            raise NotImplementedError

    def _run_pipeline(self) -> bool:
        return

    def _ingest_globally(self) -> bool:
        print("Ingesting folder globally")
        return DicomIngestController.ingest_globally(
            folder=self.folder.relative_to(config.UPLOAD_DIR).as_posix(),
            calling_aet=self.calling_aet,
            calling_host=self.calling_host,
            calling_port=self.calling_port
        )

    def _ingest_to_user(self):
        username = utils.strip_prefix(self.called_aet, config.USER_AE_PREFIX)
        query_user = self._db.query(User) \
            .filter_by(username=username) \
            .first()

        if not query_user:
            print(f"ERROR: Attempted to ingest to non-existant user {username}")
            raise NotImplementedError

        print(f"Ingesting folder to user: '{query_user.username}'")
        return DicomIngestController.ingest_to_user(
            folder=self.folder.relative_to(config.UPLOAD_DIR).as_posix(),
            calling_aet=self.calling_aet,
            calling_host=self.calling_host,
            calling_port=self.calling_port,
            user_id=query_user.id
        )

    def _ingest_through_pipeline(self) -> bool:
        ae_title = utils.strip_prefix(self.called_aet, config.PIPELINE_AE_PREFIX)
        pipeline = self._db.query(Pipeline).filter_by(ae_title=ae_title).first()
        folder = self.folder

        if not pipeline:
            print(f"ERROR: Attempted to ingest to non-existant pipeline {ae_title}")
            raise NotImplementedError

        conditions_service = PipelineConditionService(pipeline, self.initiator_node, self._db)
        # print(conditions_service.has_conditions())
        if conditions_service.has_conditions():
            # Add to a temp folder
            conditions_service.add_series_to_storage_bucket(self.folder)

            # Run if all the conditions are satisfied
            if not conditions_service.are_conditions_met():
                print(f"Waiting for more files before running pipeline: '{pipeline.ae_title}'")
                return False

            # Updating to the bucket's folder
            folder = conditions_service.storage_bucket.get_abs_path()

        print(f"Running folder through pipeline: '{pipeline.ae_title}'")
        return PipelineController.run_pipeline_on_folder(
            db=self._db,
            pipeline_id=pipeline.id,
            folder=pathlib.Path(folder),
            initiator_dicom_node_id=self.initiator_node.id
        )
