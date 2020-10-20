from typing import List, Optional
from pydantic import validator

from . import BaseModel, BaseORMModel
from .container import Container


class PipelineNodeCreate(BaseModel):
    node_id: int
    container_id: int
    x: int
    y: int
    container_is_input: bool
    container_is_output: bool


class PipelineNode(BaseORMModel):
    pipeline_id: int
    container_id: int
    x_coord: int
    y_coord: int
    container_is_input: bool
    container_is_output: bool
    container: Container


class PipelineLinkCreate(BaseModel):
    to: int
    from_: int

    class Config:
        fields = {
            'from_': 'from'
        }


class PipelineLink(BaseORMModel):
    pipeline_id: int
    to_node_id: int
    from_node_id: int


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
    nodes: Optional[List[PipelineNode]] = []
    links: Optional[List[PipelineLink]] = []


class PipelineId(BaseModel):
    pipeline_id: int


DICOM_TYPES = ['node', 'patient', 'study', 'series']


class PipelineRunOptions(BaseModel):
    dicom_obj_type: str
    dicom_obj_id: str

    class Config:
        schema_extra = {
            "example": {
                "dicom_obj_type": "study",
                "dicom_obj_id": "some study id",
            }
        }

    @validator('dicom_obj_type')
    def type_must_be(cls, v: str):
        if v := v.lower() not in DICOM_TYPES:
            raise ValueError(f'{v} is not a valid type. Valid types are {DICOM_TYPES}')
        return v
