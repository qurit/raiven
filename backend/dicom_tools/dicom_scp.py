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

def handle_store(event):
    """Handle EVT_C_STORE events."""
    print(event)
    print(event.assoc.requestor.address)
    print(event.assoc.requestor.port)
    title = str(event.assoc.requestor.ae_title, encoding='utf-8').strip()
    newAE = models.dicom.ApplicationEntity(title=title)
    print(session)
    session.add(newAE)
    session.commit()
    # print(newAE.title)
    # print(newAE)
    # print(db)
    # print(type(db))
    
    # db.add(newAE)
    # application_entity = schemas.ApplicationEntityCreate()
    # application_entity.title = title
    # save_ae(title, newAE)

    # dicom_store = models.dicom.ApplicationEntityCreate(title=title)
    # db.add(dicom_store)
    # db.commit()

    # ds = event.dataset
    # ds.file_meta = event.file_meta
    # ds.save_as(ds.SOPInstanceUID, write_like_original=False)
    # models.dicom.ApplicationEntity(title)
    # print(ds)
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