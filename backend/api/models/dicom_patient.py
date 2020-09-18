from sqlalchemy import *

from api import db, config
from .schemas import add_schema


@add_schema
class DicomPatient(db.Model):
    id = Column(Integer, primary_key=True)
    dicom_store_id = Column(Integer)

    def __repr__(self):
        return '<DicomPatient {}>'.format(self.id)
