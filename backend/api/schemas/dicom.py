from . import BaseModel, BaseORMModel
from typing import Optional, List
from datetime import datetime


class DicomStats(BaseModel):
    dicom_node_counts: int
    dicom_patient_counts: int
    dicom_study_counts: int
    dicom_series_counts: int


class DicomSeries(BaseORMModel):
    dicom_study_id: int
    series_instance_uid: str
    series_description: str
    modality: str
    date_received: datetime


class DicomStudy(BaseORMModel):
    dicom_patient_id: int
    study_instance_uid: str
    study_date: datetime


class DicomPatient(BaseORMModel):
    patient_id: str
    dicom_node_id: int


class DicomNode(BaseORMModel):
    title: str
    host: str
    port: int
    output: bool = False
    input: bool = False
    user_id: Optional[int] = None


class DicomNodeCreate(BaseModel):
    title: str
    host: str
    port: int
    output: Optional[bool] = False
    input: Optional[bool] = False
