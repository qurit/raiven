import pathlib
from os import PathLike
from typing import Union

from api import config
from api.models import utils
from api.models.pipeline import PipelineRun

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
    def pipeline_run_factory(db, dicom_cls, dicom_obj_id, pipeline_id) -> PipelineRun:
        run = PipelineRun(pipeline_id=pipeline_id)
        run.save(db)

        input_data_model = dicom_cls.query(db).get(dicom_obj_id)
        utils.copy_model_fs(input_data_model, run)

        return run


class DicomIngestController:

    @staticmethod
    def ingest_folder(folder: pathlib.Path, calling_aet: str, calling_host: str, calling_port: int, called_aet: str):
        rel_folder: str = folder.relative_to(config.UPLOAD_DIR).as_posix()

        # TODO: Finish logic here.

        # Pushed globally
        if called_aet == config.SCP_AE_TITLE:
            args = (rel_folder, calling_aet, calling_host, calling_port)
            ingest.run_ingest_task.send_with_options(args=args)

        # Pushed to user
        elif called_aet.startswith(config.USER_AE_PREFIX):
            raise NotImplementedError

        # Pushed to pipeline
        elif called_aet.startswith(config.PIPELINE_AE_PREFIX):
            raise NotImplementedError

        # Pushed to an undefined location
        else:
            raise NotImplementedError
