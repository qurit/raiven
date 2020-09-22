from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime


from api import db, config
from .schemas import add_schema
from api.models.application_entity import ApplicationEntity


@add_schema
class DicomStoreEvent(db.Model):
    id = Column(Integer, primary_key=True)
    application_entity_id = Column(Integer, ForeignKey('application_entity.id', ondelete='CASCADE'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    path = Column(String)

    application_entity = relationship('ApplicationEntity')

    def __repr__(self):
        return '<DicomStoreEvent {}>'.format(self.id)
