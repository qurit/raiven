from api.models import pipeline as models, utils
from api.schemas import pipeline as schemas
from api import pipelining

from . import BaseController


class PipelineController(BaseController):

    @staticmethod
    def run_pipeline_task(pipeline_run_id):
        pipelining.run_pipeline(pipeline_run_id)

    def create_pipeline_run(self, options: schemas.PipelineRunOptions) -> models.PipelineRun:
        input_type = options.get_cls_type()
        input_id = options.dicom_obj_id

        run = models.PipelineRun(pipeline_id=options.pipeline_id)
        run.save(self.db)

        input_data_model = input_type.query(self.db).get(input_id)
        utils.copy_model_fs(input_data_model, run)

        return run

