from sqlalchemy import *

from api import db, config
from .schemas import add_schema


@add_schema
class DicomSeries(db.Model):
    id = Column(Integer, primary_key=True)
    dicom_study_id = Column(Integer)
    series_instance_uid = Column(String)
    series_description = Column(String)
    modality = Column(String)
    path = Column(String)

    def __repr__(self):
        return '<DicomSeries {}>'.format(self.id)
