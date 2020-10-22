from . import BaseModel, BaseORMModel
from typing import Optional, List
from datetime import datetime


class DicomSeries(BaseORMModel):
    dicom_study_id: int
    series_instance_uid: str
    series_description: str
    modality: str


class DicomStudy(BaseORMModel):
    dicom_patient_id: int
    study_instance_uid: str
    study_date: datetime
    # series: Optional[List[DicomSeries]]


class DicomPatient(BaseORMModel):
    patient_id: str
    dicom_node_id: int
    # studies: Optional[List[DicomStudy]]


class DicomNode(BaseORMModel):
    title: str
    host: str
    port: int
    # patients: Optional[List[DicomPatient]]
