from sqlalchemy import *
from datetime import datetime

from api import db, config
from .schemas import add_schema


@add_schema
class DicomStoreEvent(db.Model):
    id = Column(Integer, primary_key=True)
    application_entity_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    path = Column(String)

    def __repr__(self):
        return '<DicomStoreEvent {}>'.format(self.id)
