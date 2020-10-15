import os

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from typing import List

from api import session
from api.schemas import dicom
from api.models.dicom import DicomNode, DicomPatient, DicomSeries, DicomStudy


router = APIRouter()


@router.get("/nodes", response_model=List[dicom.DicomNode])
def get_all_dicom_nodes(db: Session = Depends(session)):
    return db.query(DicomNode).all()


@router.put("/node/{dicom_node_id}")
def send_dicom_node(dicom_node_id: int, db: Session = Depends(session)):
    dicom_node = db.query(DicomNode).get(dicom_node_id)
    return(dicom_node.abs_path)


@router.put("/node/{dicom_node_id}/{dicom_patient_id}")
def send_dicom_patient(dicom_node_id: int, dicom_patient_id: int, db: Session = Depends(session)):
    dicom_patient = db.query(DicomPatient).get(dicom_patient_id)
    return(dicom_patient.abs_path)


@router.put("/node/{dicom_node_id}/{dicom_patient_id}/{dicom_study_id}")
def send_dicom_study(dicom_node_id: int, dicom_patient_id: int, dicom_study_id: int, db: Session = Depends(session)):
    dicom_study = db.query(DicomStudy).get(dicom_study_id)
    return(dicom_study.abs_path)


@router.put("/node/{dicom_node_id}/{dicom_patient_id}/{dicom_study_id}/{dicom_series_id}")
def send_dicom_series(dicom_node_id: int, dicom_patient_id: int, dicom_study_id: int, dicom_series_id: int, db: Session = Depends(session)):
    dicom_series = db.query(DicomSeries).get(dicom_series_id)
    return(dicom_series.abs_path)
