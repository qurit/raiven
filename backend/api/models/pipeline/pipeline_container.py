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
    description = Column(String)


class Pipeline(Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)

    pipeline_containers = relationship("PipelineContainer", backref="pipeline")

    def starting_containers(self):
        return [c for c in self.containers if c.is_root_node()]


class PipelineNode(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    container_id = Column(ForeignKey("container.id"))
    x_coord = Column(Integer)
    y_coord = Column(Integer)

    next_links = relationship('PipelineLink', foreign_keys='PipelineLink.input_pipeline_container_id')
    previous_links = relationship('PipelineLink', foreign_keys='PipelineLink.output_pipeline_container_id')

    def is_root_node(self):
        return not len(self.previous_links)

    def is_leaf_node(self):
        return not len(self.next_links)


class PipelineLink(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    to_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))
    from_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))


class PipelineRun(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    complete = Column(Boolean, default=False)
    start_datetime = Column(DateTime)