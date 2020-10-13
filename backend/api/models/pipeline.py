from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import config
from . import Base, PathMixin


class Pipeline(Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)

    nodes = relationship("PipelineNode", backref="pipeline")
    links = relationship("PipelineLink", backref="pipeline")

    def starting_containers(self):
        return [c for c in self.containers if c.is_root_node()]


class PipelineNode(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    container_id = Column(ForeignKey("container.id"))
    x_coord = Column(Integer)
    y_coord = Column(Integer)

    next_links = relationship('PipelineLink', foreign_keys='PipelineLink.to_node_id')
    previous_links = relationship('PipelineLink', foreign_keys='PipelineLink.from_node_id')

    def is_root_node(self):
        return not len(self.previous_links)

    def is_leaf_node(self):
        return not len(self.next_links)


class PipelineLink(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    to_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))
    from_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))


class PipelineJob(PathMixin):
    pipeline_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))
    status = Column(String)
    path = Column(String)
