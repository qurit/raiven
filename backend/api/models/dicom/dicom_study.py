from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime

from .. import Base


class DicomStudy(Base):
    id = Column(Integer, primary_key=True)
    dicom_patient_id = Column(Integer, ForeignKey("dicom_patient.id", ondelete='CASCADE'))
    study_instance_uid = Column(String)
    study_date = Column(DateTime)

    dicom_patient = relationship('DicomPatient')

    def __repr__(self):
        return '<DicomStudy {}>'.format(self.id)
