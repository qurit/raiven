from sqlalchemy import *

from api import db, config
from .schemas import add_schema

# TODO FIX THE FOREIGN KEYS AND STUFF FORGOT ABOUT IT RIP 

@add_schema
class ApplicationEntity(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __repr__(self):
        return '<ApplicationEntity {}>'.format(self.title)
