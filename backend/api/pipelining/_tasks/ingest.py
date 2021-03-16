import pathlib
import shutil
from datetime import datetime

from pydicom import dcmread

from api import worker_session, config
from api.models.dicom import DicomNode, DicomPatient, DicomStudy, DicomSeries
from . import dramatiq


@dramatiq.actor(max_retries=0)
def run_ingest_task(folder: str, dicom_node_id: int, user_id: int = None):
    """
    The models will automatically create the folders because they inherit from NestedPathMixin found in database.py
    Speed can be improved by starting query from series (requires joins) but will cut the avg amount of queries down
    from n=4 to n=1. Calculating the storage path could be faster by not using lazy relationships in the NestedPathMixin
    """
    print("BACKEND INGEST")
    folder = pathlib.Path(config.UPLOAD_DIR) / folder

    # TODO: should we put this in the loop instead and make more, shorter connections?
    with worker_session() as db:
        node: DicomNode = db.query(DicomNode).get(dicom_node_id)

        # Getting the user specific node
        if user_id:
            node = update_or_create_user_node(db, node, user_id)

        for file_path in folder.glob('**/*.dcm'):
            ds = dcmread(str(file_path))

            if not (patient := db.query(DicomPatient).filter_by(dicom_node_id=node.id, patient_id=ds.PatientID).first()):
                patient = DicomPatient(dicom_node_id=node.id, patient_id=ds.PatientID)
                patient.save(db)

            if not (study := db.query(DicomStudy).filter_by(dicom_patient_id=patient.id, study_instance_uid=ds.StudyInstanceUID).first()):
                study = DicomStudy(
                    dicom_patient_id=patient.id,
                    study_instance_uid=ds.StudyInstanceUID,
                    study_date=datetime.strptime(ds.StudyDate + ds.StudyTime, '%Y%m%d%H%M%S')
                )
                study.save(db)

            if not (series := db.query(DicomSeries).filter_by(dicom_study_id=study.id, series_instance_uid=ds.SeriesInstanceUID).first()):
                series = DicomSeries(
                    dicom_study_id=study.id,
                    series_instance_uid=ds.SeriesInstanceUID,
                    # TODO: Add a series description table
                    series_description=ds.SeriesDescription,
                    modality=ds.Modality,
                    date_received=datetime.today()

                )
                series.save(db)

            # Grab the save path so we can release the session connection
            save_path = pathlib.Path(series.get_abs_path()) / (ds.SOPInstanceUID + '.dcm')
            shutil.move(file_path, save_path)
        db.commit()

    shutil.rmtree(folder)


def update_or_create_user_node(db, global_node: DicomNode, user_id: int) -> DicomNode:
    if node := DicomNode.query(db).filter_by(title=global_node.title, host=global_node.host, user_id=user_id).first():
        node.last_connected = datetime.utcnow()
    else:
        node = DicomNode(
            title=global_node.title,
            host=global_node.host,
            user_id=user_id,
            first_connected=datetime.utcnow(),
            last_connected=datetime.utcnow(),
            implementation_version_name=global_node.implementation_version_name,
            input=True,
        ).save(db)

    return node

