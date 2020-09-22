from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import db, config
from .schemas import add_schema
from api.models.dicom_study import DicomStudy


@add_schema
class DicomSeries(db.Model):
    id = Column(Integer, primary_key=True)
    dicom_study_id = Column(Integer, ForeignKey("dicom_study.id", ondelete="CASCADE"))
    series_instance_uid = Column(String)
    series_description = Column(String)
    modality = Column(String)
    path = Column(String)

    dicom_study = relationship('DicomStudy')

    def __repr__(self):
        return '<DicomSeries {}>'.format(self.id)
