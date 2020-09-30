import os

from sqlalchemy import *
from sqlalchemy.orm import relationship

from . import Base, PathMixin, NestedPathMixin


class DicomNode(PathMixin, Base):
    title = Column(String)
    host = Column(String)
    port = Column(Integer)


class DicomPatient(NestedPathMixin, Base):
    dicom_node_id = Column(Integer, ForeignKey("dicom_node_id.id", ondelete="CASCADE"))
    study_instance_id = Column(String)

    node = relationship('DicomNode')

    @property
    def path(self) -> str:
        return os.path.join(self.node.path, self.id)


class DicomStudy(NestedPathMixin, Base):
    dicom_patient_id = Column(Integer, ForeignKey("dicom_patient.id", ondelete='CASCADE'))
    study_instance_uid = Column(String)
    study_date = Column(DateTime)

    patient = relationship('DicomPatient')

    @property
    def path(self) -> str:
        return os.path.join(self.patient.path, self.id)


class DicomSeries(NestedPathMixin, Base):
    dicom_study_id = Column(Integer, ForeignKey("dicom_study.id", ondelete="CASCADE"))
    series_instance_uid = Column(String)
    series_description = Column(String)
    modality = Column(String)

    study = relationship('DicomStudy')

    @property
    def path(self) -> str:
        return os.path.join(self.study.path, self.id)


