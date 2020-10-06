from typing import List, Optional

from . import BaseModel, BaseORMModel


class PipelineContainerCreate(BaseModel):
    pipeline_id: int
    container_id: int
    x_coord: int
    y_coord: int

    # this stuff
    # next_links: Optional[List[int]]
    # previous_links: Optional[List[int]]


class PipelineLinkCreate(BaseModel):
    pipeline_id: int
    input_pipeline_container_id: Optional[int]
    output_pipeline_container_id: Optional[int]


class PipelineLink(PipelineLinkCreate, BaseORMModel):
    pass


class PipelineContainer(PipelineContainerCreate, BaseORMModel):
    pass


class PipelineCreate(BaseModel):
    name: str


class Pipeline(PipelineCreate, BaseORMModel):
    user_id: Optional[int]
    pipeline_containers: Optional[List[PipelineContainer]] = []


class PipelineFull(Pipeline):
    pass

# TODO: to delete, added just for now to get container to work


class UserCreate(BaseModel):
    username: str
    name = str
    title = str
    department = str
    company = str
