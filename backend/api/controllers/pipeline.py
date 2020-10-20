from api.models import pipeline as models, utils
from api.schemas import pipeline as schemas

from . import BaseController


class PipelineController(BaseController):

    def run_pipeline(self, options: schemas.PipelineRunOptions):
        input_type = options.get_cls_type()
        input_id = options.dicom_obj_id

        run = models.PipelineRun()
        run.save(self.db)

        input_data_model = input_type.query(self.db).get(input_id)
        utils.copy_model_fs(input_data_model, run)

        return run

