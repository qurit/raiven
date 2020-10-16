import os

from sqlalchemy import *
from sqlalchemy.orm import relationship

from . import Base


class Destination(Base):
    host = Column(String)
    port = Column(Integer)
    full_name = Column(String)
