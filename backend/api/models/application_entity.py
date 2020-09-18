from sqlalchemy import *

from api import db, config
from .schemas import add_schema


@add_schema
class ApplicationEntity(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __repr__(self):
        return '<ApplicationEntity {}>'.format(self.title)
