import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi import Depends
from pydantic import BaseModel

# from . import models, schemas

from api import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

from api import models, schemas
print("FJFJSFJSFJSFJSFJSFJSFJSFJSFJSFJ")
print(session)
print(Depends)

from pynetdicom import (
    AE, debug_logger, evt, AllStoragePresentationContexts,
    ALL_TRANSFER_SYNTAXES
)
# from backend.api import db
debug_logger()

# def save_ae(title, application_entity: schemas.ApplicationEntityCreate, db: Session = Depends(session)):
#     # print(db)
#     # print(ae)
#     # print(type(db))
#     # models.dicom.ApplicationEntity(title=title).save(db)
#     # db.add(dicom_store)
#     # db.commit()

#     newAE = models.dicom.ApplicationEntity(title=application_entity.title)
#     db.add(newAE)
#     db.commit()
#     db.refresh(newAE)
#     return newAE

# TODO: make helper functions to add the dicom patient / study/ other stuff 
# to the database so its not all one big thing? 
def handle_store(event):
    """Handle EVT_C_STORE events."""
    print(event)
    print(event.dataset)
    patient = event.dataset.PatientID
    studyInstanceUID = event.dataset.StudyInstanceUID
    studyDate = event.dataset.StudyDate
    print(event.dataset.SeriesInstanceUID)
    print(event.dataset.Modality)
    # print(event.dataset.SeriesDescription)
    host = event.assoc.requestor.address
    port = event.assoc.requestor.port
    title = str(event.assoc.requestor.ae_title, encoding='utf-8').strip()
    newAE = models.dicom.ApplicationEntity(title=title)
    # newPatient = models.dicom.DicomPatient(id=123123)
    # session.add(newPatient)
    # session.commit()
    session.add(newAE)
    session.commit()

    event.dataset.file_meta = event.file_meta
    event.dataset.save_as(event.dataset.SOPInstanceUID, write_like_original=False)
    
    ds = event.dataset
    path = os.path.join(os.getcwd(), 'tmp')
    if not os.path.exists(path):
        os.mkdir(path)
    print(path)
    path = os.path.join(path, ds.PatientID)
    if not os.path.exists(path):
        print("make patient folder")
        os.mkdir(path)

    path = os.path.join(path, ds.StudyInstanceUID)
    if not os.path.exists(path):
        print("make study folder")
        os.mkdir(path)
    path = os.path.join(path, ds.SeriesInstanceUID)
    if not os.path.exists(path):
        print("make series folder")
        os.mkdir(path)

    path = os.path.join(path, ds.SOPInstanceUID + '.dcm')
    ds.save_as(path, write_like_original=False)
    print( 'saved image at', path)
    
    newDicomStoreEvent = models.dicom.DicomStoreEvent(path=path)
    session.add(newDicomStoreEvent)
    session.commit()

    print(os.getcwd())
    print("BLAHBLAHBLAH")
    # print(ds.PatientID)
    # TMP_DIR = os.path.join(os.getcwd(), 'tmp')
    # path = os.path.join(TMP_DIR, ds.PatientId)
    # if not os.path.exists(path):
    #     os.mkdir(path)
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()
storage_sop_classes = [
     cx.abstract_syntax for cx in AllStoragePresentationContexts
]
for uid in storage_sop_classes:
    ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)

ae.start_server(('', 11112), block=True, evt_handlers=handlers)