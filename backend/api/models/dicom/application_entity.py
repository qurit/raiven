from sqlalchemy import *

from .. import Base

# TODO FIX THE FOREIGN KEYS AND STUFF FORGOT ABOUT IT RIP 


class ApplicationEntity(Base):
    title = Column(String)

    def __repr__(self):
        return '<ApplicationEntity {}>'.format(self.title)
