from os import PathLike
from typing import Union

from api.models import pipeline as models, utils
from api.schemas import pipeline as schemas

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
    def ingest_folder(folder: Union[str, PathLike], calling_aet: str, calling_host: str, calling_port: int, called_aet: str):
        # TODO: Finish logic here.

        # Pushed globally
        if called_aet == config.SCP_AE_TITLE:
            args = (folder, calling_aet, calling_host, calling_port)
            ingest.run_ingest_task.send(args=args)

        # Pushed to user
        elif called_aet.startswith(config.USER_AE_PREFIX):
            raise NotImplementedError

        # Pushed to pipeline
        elif called_aet.startswith(config.PIPELINE_AE_PREFIX):
            raise NotImplementedError

        # Pushed to an undefined location
        else:
            raise NotImplementedError
