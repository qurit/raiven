from pynetdicom import AE, evt
from pynetdicom.presentation import AllStoragePresentationContexts
from pynetdicom.sop_class import VerificationSOPClass

from api import config
from api.models.dicom import DicomNode, DicomPatient, DicomStudy, DicomSeries


def get_ae_title(event):
    return str(event.assoc.requestor.ae_title, encoding='utf-8').strip()


def handle_store(event):
    """ Handles EVT_C_STORE """
    print("STORE EVENT")

    ae_title = get_ae_title(event)
    # host = event.assoc.requestor.address
    # port = event.assoc.requestor.port

    ds = event.dataset

    with session() as db:
        print("HERE")

        """ 
        The models will automatically create the folders because they inherit from NestedPathMixin found in database.py
        Speed can be improved by starting query from series (requires joins) but will cut the avg amount of queries down
        from n=4 to n=1
        """

        # TODO: SHOULD START WITH SERIES FOR MORE EFFICIENCY
        if not (node := db.query(DicomNode).filter_by(title=ae_title).first()):
            node = DicomNode(
                title=ae_title
                # TODO: add port / host
            ).save(db)
            print("Node created")

        if not (patient := db.query(Patient).filter_by(dicom_node_id=node.id, patient_id=ds.PatientID).first()):
            patient = Patient(
                dicom_node_id=node.id,
                study_instance=ds.PatientID
            ).save(db)
            print("Patient created")

        if not (study := db.query(Study).filter_by(dicom_patient_id=patient_id.id, study_instance_uid=ds.StudyInstanceUID).first()):
            study = Study(
                dicom_patient_id=patient.id,
                study_instance=ds.StudyInstanceUID
                # TODO: add study date
            ).save(db)
            print("Study created")

        if not (series := db.query(Series).filter_by(dicom_study_id=study.id, series_instance_uid=ds.StudyInstanceUID).first()):
            series = Series(
                dicom_study_id=study.id,
                series_instance_uid=ds.StudyInstanceUID,
                series_description=ds.SeriesDescription, # TODO: Add a series description table
                modality=ds.Modality,
            ).save(db)
            print("Series created")

        # Grab the save path so we can release the session connection
        save_path = series.abs_path
        print(save_path)

    ds.save_as(save_path)
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