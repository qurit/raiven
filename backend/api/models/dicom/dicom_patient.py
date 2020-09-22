from sqlalchemy import *
from sqlalchemy.orm import relationship

from api.models import BaseModel


class DicomPatient(BaseModel):
    id = Column(Integer, primary_key=True)
    dicom_store_event_id = Column(Integer, ForeignKey("dicom_store_event.id", ondelete="CASCADE"))

    dicom_store_event = relationship('DicomStoreEvent')

    def __repr__(self):
        return '<DicomPatient {}>'.format(self.id)
