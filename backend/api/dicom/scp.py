import os
import datetime

from pynetdicom import AE, evt, debug_logger
from pynetdicom.presentation import AllStoragePresentationContexts
from pynetdicom.sop_class import VerificationSOPClass
from pydicom import uid

from api import config
from api.database import worker_session as session
from api.models.dicom import DicomNode, DicomPatient, DicomStudy, DicomSeries


def get_ae_title(event):
    return str(event.assoc.requestor.ae_title, encoding='utf-8').strip()


def handle_store(event):
    """ Handles EVT_C_STORE """
    ae_title = get_ae_title(event)
    ds = event.dataset
    ds.file_meta = event.file_meta
    ds.file_meta.TransferSyntaxUID = uid.ImplicitVRLittleEndian

    with session() as db:
        """
        The models will automatically create the folders because they inherit from NestedPathMixin found in database.py
        Speed can be improved by starting query from series (requires joins) but will cut the avg amount of queries down
        from n=4 to n=1. Calculating the storage path could be faster by not using lazy relationships in the NestedPathMixin
        """

        # TODO: SHOULD START WITH SERIES FOR MORE EFFICIENCY
        if not (node := db.query(DicomNode).filter_by(title=ae_title).first()):
            node = DicomNode(
                title=ae_title,
                host=event.assoc.requestor.address,
                port=event.assoc.requestor.port
            )
            node.save(db)

        if not (patient := db.query(DicomPatient).filter_by(dicom_node_id=node.id, patient_id=ds.PatientID).first()):
            patient = DicomPatient(
                dicom_node_id=node.id,
                patient_id=ds.PatientID
            )
            patient.save(db)

        if not (study := db.query(DicomStudy).filter_by(dicom_patient_id=patient.id, study_instance_uid=ds.StudyInstanceUID).first()):
            raw_date_time = ds.StudyDate + ds.StudyTime
            formatted_date_time = datetime.datetime.strptime(
                raw_date_time, '%Y%m%d%H%M%S')
            study = DicomStudy(
                dicom_patient_id=patient.id,
                study_instance_uid=ds.StudyInstanceUID,
                study_date=formatted_date_time
            )
            study.save(db)

        if not (series := db.query(DicomSeries).filter_by(dicom_study_id=study.id, series_instance_uid=ds.SeriesInstanceUID).first()):
            series = DicomSeries(
                dicom_study_id=study.id,
                series_instance_uid=ds.SeriesInstanceUID,
                # TODO: Add a series description table
                series_description=ds.SeriesDescription,
                modality=ds.Modality,
                date_received=datetime.datetime.today()

            )
            series.save(db)

        # Grab the save path so we can release the session connection
        save_path = series.get_abs_path()

    ds.save_as(os.path.join(save_path, ds.SOPInstanceUID + '.dcm'),
               write_like_original=False)

    return 0x0000


class SCP:

    def __init__(self, ae_title='PICOM_SCP', host='localhost', port=11112, debug=False):
        self.ae_title = ae_title
        self.host = host
        self.port = port

        self._ae = AE(ae_title)
        self._ae.supported_contexts = AllStoragePresentationContexts
        self._ae.add_supported_context(VerificationSOPClass)

        if debug:
            debug_logger()

    def start_server(self, blocking=False):
        handlers = [(evt.EVT_C_STORE, handle_store)]
        self._ae.start_server((self.host, self.port),
                              block=blocking, evt_handlers=handlers)

    def stop_server(self):
        self._ae.shutdown()

    def get_ae(self) -> AE:
        return self._ae


if __name__ == '__main__':
    print("Starting server...")
    print("Waiting for connections...")
    scp = SCP()
    scp.start_server(blocking=False)
    scp.stop_server()
