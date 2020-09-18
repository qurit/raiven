from sqlalchemy import *
from datetime import datetime

from api import db, config
from .schemas import add_schema


@add_schema
class DicomStudy(db.Model):
    id = Column(Integer, primary_key=True)
    dicom_patient_id = Column(Integer)
    study_instance_uid = Column(String)
    study_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<DicomStudy {}>'.format(self.id)
