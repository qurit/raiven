import os

from sqlalchemy import *
from sqlalchemy.orm import relationship

from . import Base, PathMixin, NestedPathMixin, CASCADE


class DicomNode(PathMixin, Base):
    title = Column(String)
    host = Column(String)
    port = Column(Integer)

    patients = relationship('DicomPatient', backref='node')


class DicomPatient(NestedPathMixin, Base):
    dicom_node_id = Column(Integer, ForeignKey("dicom_node.id", **CASCADE))
    patient_id = Column(String)

    studies = relationship('DicomStudy', backref='patient')

    def get_path(self) -> str:
        return os.path.join(self.node.get_path(), str(self.id))


class DicomStudy(NestedPathMixin, Base):
    dicom_patient_id = Column(Integer, ForeignKey("dicom_patient.id", **CASCADE))
    study_instance_uid = Column(String)
    study_date = Column(DateTime)

    series = relationship('DicomSeries', backref='study')

    def get_path(self) -> str:
        return os.path.join(self.patient.get_path(), str(self.id))


class DicomSeries(NestedPathMixin, Base):
    dicom_study_id = Column(Integer, ForeignKey("dicom_study.id", **CASCADE))
    series_instance_uid = Column(String)
    series_description = Column(String)
    modality = Column(String)
    date_received = Column(DateTime)

    def get_path(self) -> str:
        return os.path.join(self.study.get_path(), str(self.id))
