from api.models import pipeline as models, utils
from api.schemas import pipeline as schemas

from api.models.pipeline import PipelineRun
from ._tasks import build, run


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
