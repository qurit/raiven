from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import config
from . import Base, PathMixin, TimestampMixin
from api.models.pipeline import PipelineNode


class Container(PathMixin, Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)
    dockerfile_path = Column(String)
    is_input_container = Column(Boolean)
    is_output_container = Column(Boolean)
    description = Column(String)
    # filename = Column(String)

    # TODO: This doesnt make sense
    container = relationship(
        'PipelineNode', foreign_keys='PipelineNode.container_id')


class ContainerBuild(TimestampMixin, Base):
    container_id = Column(ForeignKey("container.id", ondelete="CASCADE"))
    exit_code = Column(Integer)
    tag = Column(String)

    error = relationship('ContainerBuildError', uselist=False, backref='build')


class ContainerBuildError(Base):
    container_id = Column(ForeignKey("container_build.id", ondelete="CASCADE"))
    stderr = Column(String)
