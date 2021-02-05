import pathlib
import shutil

from api import config
from api.database import worker_session
from api.models import utils
from api.models.dicom import DicomNode
from api.models.pipeline import Pipeline, PipelineRun
from api.models.user import User
from ._tasks import build, run, test, ingest


def run_test_task():
    test.run_test_task.send()


class ContainerController:

    @staticmethod
    def build_container(container_id: int, priority: int = 1):
        build.build_container_task.send_with_options(args=(container_id,), priority=priority)


class PipelineController:

    @staticmethod
    def run_pipeline_task(db, pipeline_run: PipelineRun, priority: int = 1) -> bool:
        pipeline_run.status = 'running'
        pipeline_run.save(db)
        db.commit()

        for node in pipeline_run.pipeline.get_starting_nodes():
            task = run.dicom_output_task if node.container_is_output else run.run_node_task
            args = pipeline_run.id, node.id

            print(task)
            task.send_with_options(args=args, priority=priority)

        return True

    @staticmethod
    def run_pipeline_on_folder(db, pipeline_id: str, folder: pathlib.Path, initiator_dicom_node_id: int = None) -> bool:
        pipeline_run = PipelineRun(pipeline_id=pipeline_id, initiator_id=initiator_dicom_node_id)
        pipeline_run.save(db)

        # Copy temp files to pipeline input and commit
        shutil.copytree(folder.resolve(), pipeline_run.get_abs_input_path(), dirs_exist_ok=True)
        shutil.rmtree(folder.resolve())
        db.commit()

        return PipelineController.run_pipeline_task(db, pipeline_run)

    @staticmethod
    def pipeline_run_factory(db, dicom_cls, dicom_obj_id, pipeline_id) -> PipelineRun:
        pipeline_run = PipelineRun(pipeline_id=pipeline_id)
        pipeline_run.save(db)

        input_data_model = dicom_cls.query(db).get(dicom_obj_id)
        utils.copy_model_fs(input_data_model, pipeline_run)

        return pipeline_run


class DicomIngestController:

    class EmptyFolderException(Exception):
        pass

    def __init__(self, folder: pathlib.Path, calling_aet: str, calling_host: str, calling_port: int, called_aet: str):
        if not any(folder.iterdir()):
            shutil.rmtree(folder.resolve())

            print("INFO: Empty ingested folder")
            raise self.EmptyFolderException('An Ingest Folder Cannot Be Empty')

        self.folder = folder
        self.calling_aet = calling_aet
        self.calling_host = calling_host
        self.calling_port = calling_port
        self.called_aet = called_aet

        # Pushed globally
        if self.called_aet == config.SCP_AE_TITLE:
            self.ingest_globally()

        # Pushed to user
        elif self.called_aet.startswith(config.USER_AE_PREFIX):
            self.ingest_to_user()

        # Pushed to pipeline
        elif self.called_aet.startswith(config.PIPELINE_AE_PREFIX):
            self.ingest_through_pipeline()

        # Pushed to an undefined location
        else:
            print("ERROR: Undefined called AET")
            raise NotImplementedError

    def ingest_globally(self) -> bool:
        print("Ingesting folder globally")
        rel_folder: str = self.folder.relative_to(config.UPLOAD_DIR).as_posix()
        args = (rel_folder, self.calling_aet, self.calling_host, self.calling_port)
        ingest.run_ingest_task.send_with_options(args=args)
        return True

    def ingest_to_user(self):
        with worker_session() as db:
            # Get user id from username
            username = utils.strip_prefix(self.called_aet, config.USER_AE_PREFIX)
            query_user = db.query(User)\
                .filter_by(username=username)\
                .first()

            if query_user:
                print(f"Ingesting folder to user: '{query_user.username}'")
                rel_folder: str = self.folder.relative_to(config.UPLOAD_DIR).as_posix()
                args = (rel_folder, self.calling_aet, self.calling_host, self.calling_port, query_user.id)
                ingest.run_ingest_task.send_with_options(args=args)
                return True
            else:
                print("ERROR: Attempted to ingest to non-existant user")
                raise NotImplementedError

    def ingest_through_pipeline(self) -> bool:
        with worker_session() as db:
            ae_title = utils.strip_prefix(self.called_aet, config.PIPELINE_AE_PREFIX)

            pipeline = db.query(Pipeline)\
                .filter_by(ae_title=ae_title)\
                .first()

            if not (initiator := db.query(DicomNode).filter_by(
                title=self.calling_aet,
                host=self.calling_host,
                port=self.calling_port,
            ).first()):

                initiator = DicomNode(
                    title=self.calling_aet,
                    host=self.calling_host,
                    port=self.calling_port,
                )

                initiator.save(db)

            if pipeline:
                print("Running folder through pipeline: '{}'".format(pipeline.ae_title))
                return PipelineController.run_pipeline_on_folder(db, pipeline.id, self.folder, initiator.id)
            else:
                print(ae_title)
                print("ERROR: Attempted to ingest to non-existant pipeline")
                raise NotImplementedError
