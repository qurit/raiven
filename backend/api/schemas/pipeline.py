from . import BaseModel, BaseORMModel


class PipelineCreate(BaseModel):
    name: str


class Pipeline(PipelineCreate, BaseORMModel):
    pass


class PipelineFull(Pipeline):
    pass


class PipelineStepCreate(BaseModel):
    pipeline_id: int
    container_id: int
    # next_pipeline_step_id: Optional[int]


class PipelineStep(PipelineStepCreate, BaseORMModel):
    pass
