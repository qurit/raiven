import os
from collections import Counter
from itertools import chain

from sqlalchemy.orm import Session
from sqlalchemy import asc
from fastapi import APIRouter, Depends
from typing import List

from api import session
from api.schemas import dicom, pipeline
from api.models.dicom import DicomNode, DicomPatient, DicomStudy, DicomSeries


router = APIRouter()


@router.get("/received-series")
def get_received_series(db: Session = Depends(session)):
    dicom_series = db.query(DicomSeries.date_received).order_by(
        asc(DicomSeries.date_received)).all()
    dicom_series_to_count = list(chain(*dicom_series))
    dicom_series_to_count = map(lambda x: x.date(), dicom_series_to_count)
    dicom_series_to_count = list(dicom_series_to_count)
    return Counter(dicom_series_to_count)


@router.get("/series-breakdown")
def get_series_breakdown(db: Session = Depends(session)):
    dicom_series = db.query(DicomSeries.modality).order_by(
        asc(DicomSeries.modality)).all()
    dicom_series_to_count = list(chain(*dicom_series))
    return Counter(dicom_series_to_count)


@router.get("/nodes", response_model=List[dicom.DicomNode])
def get_all_dicom_nodes(db: Session = Depends(session)):
    print("Here")
    return db.query(DicomNode).all()


@router.put("/node/{dicom_node_id}")
def send_dicom_node(dicom_node_id: int, pipeline_id: pipeline.PipelineId, db: Session = Depends(session)):
    print(dicom_node_id)
    print(pipeline_id)
    dicom_node = db.query(DicomNode).get(dicom_node_id)
    return(dicom_node.abs_path)


@router.put("/node/{dicom_node_id}/{dicom_patient_id}")
def send_dicom_patient(dicom_node_id: int, dicom_patient_id: int, pipeline_id: pipeline.PipelineId, db: Session = Depends(session)):
    dicom_patient = db.query(DicomPatient).get(dicom_patient_id)
    return(dicom_patient.abs_path)


@router.put("/node/{dicom_node_id}/{dicom_patient_id}/{dicom_study_id}")
def send_dicom_study(dicom_node_id: int, dicom_patient_id: int, dicom_study_id: int,   pipeline_id: pipeline.PipelineId, db: Session = Depends(session)):
    dicom_study = db.query(DicomStudy).get(dicom_study_id)
    return(dicom_study.abs_path)


@router.put("/node/{dicom_node_id}/{dicom_patient_id}/{dicom_study_id}/{dicom_series_id}")
def send_dicom_series(dicom_node_id: int, dicom_patient_id: int, dicom_study_id: int, dicom_series_id: int,  pipeline_id: pipeline.PipelineId, db: Session = Depends(session)):
    dicom_series = db.query(DicomSeries).get(dicom_series_id)
    return(dicom_series.abs_path)
