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


@router.get("/patients", response_model=List[dicom.DicomPatient])
def get_all_dicom_patients(db: Session = Depends(session)):
    return db.query(DicomPatient).all()


@router.get("/series", response_model=List[dicom.DicomSeries])
def get_all_dicom_series(db: Session = Depends(session)):
    return db.query(DicomSeries).all()


@router.get("/studies", response_model=List[dicom.DicomStudy])
def get_all_dicom_studies(db: Session = Depends(session)):
    return db.query(DicomStudy).all()
