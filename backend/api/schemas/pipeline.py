from typing import List, Optional

from . import BaseModel, BaseORMModel


class PipelineNodeCreate(BaseModel):
    node_id: int
    container_id: int
    x: int
    y: int


class PipelineNode(BaseORMModel):
    pipeline_id: int
    container_id: int
    x_coord = int
    y_coord = int


class PipelineLinkCreate(BaseModel):
    to: int
    from_: int

    class Config:
        fields = {
            'from_': 'from'
        }


class PipelineLink(BaseORMModel):
    pipeline_id = int
    to_node_id = int
    from_node_id = int


class PipelineCreate(BaseModel):
    name: str


class PipelineUpdate(BaseModel):
    pipeline_id: Optional[int]
    nodes: Optional[List[PipelineNodeCreate]] = []
    links: Optional[List[PipelineLinkCreate]] = []


class Pipeline(PipelineCreate, BaseORMModel):
    user_id: Optional[int]
    name: str


class PipelineFull(Pipeline):
    pass
    # nodes = Optional[List[PipelineNode]]
    # links = Optional[List[PipelineLink]]



