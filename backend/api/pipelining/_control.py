import pathlib
import shutil
from typing import Union

from api import config
from api.models import utils
from api.models.pipeline import Pipeline, PipelineRun
from api.database import worker_session

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
        [run.run_node_task.send_with_options(args=(pipeline_run.id, n.id,), priority=priority) for n in pipeline_run.pipeline.get_starting_nodes()]
        pipeline_run.status = 'running'
        pipeline_run.save(db)
        return True

    @staticmethod
    def run_pipeline_on_folder(db, pipeline_id: str, folder: pathlib.Path) -> bool:
        pipeline_run = PipelineRun(pipeline_id=pipeline_id)
        pipeline_run.save(db)

        # Copy temp files to pipeline input and commmit 
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

    @staticmethod
    # Returns whether or not the ingest operation successfully completed
    def ingest_folder(folder: pathlib.Path, calling_aet: str, calling_host: str, calling_port: int, called_aet: str) -> bool:
        # TODO: Finish logic here.

        # Pushed globally
        if called_aet == config.SCP_AE_TITLE:
            return DicomIngestController.ingest_globally(folder, calling_aet, calling_host, calling_port)

        # Pushed to user
        elif called_aet.startswith(config.USER_AE_PREFIX):
            return DicomIngestController.ingest_to_user()

        # Pushed to pipeline
        elif called_aet.startswith(config.PIPELINE_AE_PREFIX):
            return DicomIngestController.ingest_through_pipeline(folder, called_aet)

        # Pushed to an undefined location
        else:
            raise NotImplementedError

    @staticmethod
    def ingest_globally(folder: pathlib.Path, calling_aet: str, calling_host: str, calling_port: int) -> bool:
        print("Running ingested folder through global config")
        rel_folder: str = folder.relative_to(config.UPLOAD_DIR).as_posix()
        args = (rel_folder, calling_aet, calling_host, calling_port)
        ingest.run_ingest_task.send_with_options(args=args)
        return True

    @staticmethod
    def ingest_to_user():
        raise NotImplementedError

    @staticmethod
    def ingest_through_pipeline(folder: pathlib.Path, called_aet: str) -> bool:
        print("Running ingested folder directly on pipeline")
        with worker_session() as db:
            # Test if pipeline exists
            if not (pipeline := db.query(Pipeline).filter(Pipeline.ae_title == called_aet.strip(config.PIPELINE_AE_PREFIX)).first()):
                print("ERROR: Requested pipeline does not exist")
                raise NotImplementedError
            else:
                # Pipeline exists, Run folder through pipeline
                return PipelineController.run_pipeline_on_folder(db, pipeline.id, folder)
