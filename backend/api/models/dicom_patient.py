from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import db, config
from .schemas import add_schema
from api.models.dicom_store_event import DicomStoreEvent

@add_schema
class DicomPatient(db.Model):
    id = Column(Integer, primary_key=True)
    dicom_store_id = Column(Integer, ForeignKey("dicom_store_event.id", ondelete="CASCADE"))

    dicom_store_event = relationship('DicomStoreEvent')

    def __repr__(self):
        return '<DicomPatient {}>'.format(self.id)
