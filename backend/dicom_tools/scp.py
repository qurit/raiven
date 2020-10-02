import os

from pynetdicom import AE, evt
from pynetdicom.presentation import AllStoragePresentationContexts
from pynetdicom.sop_class import VerificationSOPClass

from api import config
from api.database import worker_session as session
from api.models.dicom import DicomNode, DicomPatient, DicomStudy, DicomSeries

print(config.UPLOAD_DIR)


def get_ae_title(event):
    return str(event.assoc.requestor.ae_title, encoding='utf-8').strip()


def handle_store(event):
    """ Handles EVT_C_STORE """
    print("STORE EVENT")

    ae_title = get_ae_title(event)
    ds = event.dataset

    try:
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
                study = DicomStudy(
                    dicom_patient_id=patient.id,
                    study_instance_uid=ds.StudyInstanceUID
                    # TODO: add study date
                )
                study.save(db)

            if not (series := db.query(DicomSeries).filter_by(dicom_study_id=study.id, series_instance_uid=ds.StudyInstanceUID).first()):
                series = DicomSeries(
                    dicom_study_id=study.id,
                    series_instance_uid=ds.StudyInstanceUID,
                    series_description=ds.SeriesDescription,  # TODO: Add a series description table
                    modality=ds.Modality,
                )
                series.save(db)

            # Grab the save path so we can release the session connection
            save_path = series.abs_path

        ds.save_as(os.path.join(save_path, ds.SOPInstanceUID + '.dcm'))
    except Exception as e:
        print(e)

    return 0x0000


if __name__ == '__main__':
    ae = AE()
    ae.supported_contexts = AllStoragePresentationContexts
    ae.add_supported_context(VerificationSOPClass)
    handlers = [
        (evt.EVT_C_STORE, handle_store),
    ]

    print("Starting server...")
    print("Waiting for connections...")
    ae.start_server(('', 11112), block=True, evt_handlers=handlers)