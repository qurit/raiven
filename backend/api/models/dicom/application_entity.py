from sqlalchemy import *

from api.models import BaseModel

# TODO FIX THE FOREIGN KEYS AND STUFF FORGOT ABOUT IT RIP 


class ApplicationEntity(BaseModel):
    title = Column(String)

    def __repr__(self):
        return '<ApplicationEntity {}>'.format(self.title)
