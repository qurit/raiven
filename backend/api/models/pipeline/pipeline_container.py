from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import config
from .. import Base, PathMixin


class Container(PathMixin, Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)
    dockerfile_path = Column(String)
    is_input_container = Column(Boolean)
    is_output_container = Column(Boolean)
    dockerfile = Column(String)


class Pipeline(Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)

    pipeline_containers = relationship("PipelineContainer", backref="pipeline")

    def starting_containers(self):
        return [c for c in self.containers if c.is_root_node()]


class PipelineContainer(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    container_id = Column(ForeignKey("container.id"))
    x_coord = Column(Integer)
    y_coord = Column(Integer)
    # next_containers_id = Column(Integer)
    # previous_containers_id = Column(Integer)

    next_container_id = relationship(
        'PipelineLink', foreign_keys='PipelineLink.input_pipeline_container_id')
    previous_container_id = relationship(
        'PipelineLink', foreign_keys='PipelineLink.output_pipeline_container_id')

    def is_root_node(self):
        return not len(self.previous_container_id)

    def is_leaf_node(self):
        return not len(self.next_container_id)


class PipelineLink(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    input_pipeline_container_id = Column(ForeignKey(
        "pipeline_container.id", ondelete="CASCADE"))
    output_pipeline_container_id = Column(ForeignKey(
        "pipeline_container.id", ondelete="CASCADE"))
