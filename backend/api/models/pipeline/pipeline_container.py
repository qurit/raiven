from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import config
from .. import Base, PathMixin


class Container(PathMixin, Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)
    dockerfile_path = Column(String)


class Pipeline(Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)


class PipelineContainer(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    container_id = Column(ForeignKey("container.id"))

    # next_steps = relationship('PipelineStep', foreign_keys=['input_container_id'])
    # previous_steps = relationship('PipelineStep', foreign_keys=['output_container_id'])


class PipelineStep(Base):
    input_container_id = Column(ForeignKey("pipeline_container.id", ondelete="CASCADE"))
    output_container_id = Column(ForeignKey("pipeline_container.id", ondelete="CASCADE"))





