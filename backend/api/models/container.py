from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import config
from . import Base, PathMixin
from api.models.pipeline import PipelineNode


class Container(PathMixin, Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)
    dockerfile_path = Column(String)
    is_input_container = Column(Boolean)
    is_output_container = Column(Boolean)
    description = Column(String)

    container = relationship(
        'PipelineNode', foreign_keys='PipelineNode.container_id')
