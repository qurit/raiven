from datetime import datetime
from typing import List, Optional
from pydantic import validator


from . import BaseModel, BaseORMModel
from .container import Container
from .destination import Destination
from api.models import dicom, Base


class PipelineNodeCreate(BaseModel):
    node_id: int
    container_id: int
    x: int
    y: int
    container_is_input: bool
    container_is_output: bool
    destination_id: Optional[int]


class PipelineNode(BaseORMModel):
    pipeline_id: int
    container_id: int
    x_coord: int
    y_coord: int
    container_is_input: bool
    container_is_output: bool
    container: Container
    destination: Optional[Destination]


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


class PipelineRunOptions(BaseModel):
    _DICOM_TYPES = {'node': dicom.DicomNode, 'patient': dicom.DicomPatient,
                    'study': dicom.DicomStudy, 'series': dicom.DicomSeries}

    pipeline_id: Optional[int]
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
        if v.lower() not in cls._DICOM_TYPES.keys():
            raise ValueError(
                f'{v} is not a valid type. Valid types are {cls.DICOM_TYPES.keys()}')
        return v

    def get_cls_type(self) -> Base:
        return self._DICOM_TYPES[self.dicom_obj_type]


class PipelineRun(BaseORMModel):
    status: str
    created_datetime: datetime
    finished_datetime: Optional[datetime]
