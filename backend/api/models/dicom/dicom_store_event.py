from sqlalchemy import *
from sqlalchemy.orm import relationship
from datetime import datetime


from .. import Base


class DicomStoreEvent(Base):
    id = Column(Integer, primary_key=True)
    application_entity_id = Column(Integer, ForeignKey('application_entity.id', ondelete='CASCADE'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    path = Column(String)

    application_entity = relationship('ApplicationEntity')

    def __repr__(self):
        return '<DicomStoreEvent {}>'.format(self.id)
