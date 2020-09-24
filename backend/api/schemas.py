from typing import List, Optional
from pydantic import BaseModel


class BaseORMModel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ApplicationEntityCreate(BaseModel):
    title: str


class ApplicationEntity(ApplicationEntityCreate, BaseORMModel):
    pass


class ContainerCreate(BaseModel):
    user_id: int
    name: str
    dockerfile_path: str


class Container(ContainerCreate, BaseORMModel):
    pass


class PipelineCreate(BaseModel):
    name: str


class Pipeline(PipelineCreate, BaseORMModel):
    pass


class PipelineStepCreate(BaseModel):
    pipeline_id: int
    container_id: int
    next_pipeline_step_id: Optional[int]


class PipelineStep(PipelineStepCreate, BaseORMModel):
    pass
