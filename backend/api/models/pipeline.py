import os
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import config
from . import Base, PathMixin, NestedPathMixin, TimestampMixin, IOPathMixin, utils


class Pipeline(Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)

    runs = relationship("PipelineRun", backref="pipeline")
    nodes = relationship("PipelineNode", backref="pipeline")
    links = relationship("PipelineLink", backref="pipeline")

    # TODO: This query can be optimized by joins
    def get_starting_nodes(self):
        return [n for n in self.nodes if n.is_root_node()]


class PipelineNode(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    container_id = Column(ForeignKey("container.id"))
    destination_id = Column(ForeignKey("destination.id"))
    x_coord = Column(Integer)
    y_coord = Column(Integer)
    container_is_input = Column(Boolean)
    container_is_output = Column(Boolean)

    container = relationship("Container", uselist=False)
    next_links = relationship('PipelineLink', foreign_keys='PipelineLink.from_node_id')
    previous_links = relationship('PipelineLink', foreign_keys='PipelineLink.to_node_id')
    jobs = relationship('PipelineJob', backref='node')
    destination = relationship('Destination', uselist=False)

    def is_root_node(self):
        return not len(self.previous_links)

    def is_leaf_node(self):
        return not len(self.next_links)

    def get_next_nodes(self):
        return [link.next_node for link in self.next_links]

    def __repr__(self, **kwargs) -> str:
        return super().__repr__(root=self.is_root_node(), leaf=self.is_leaf_node(), **kwargs)


class PipelineLink(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    to_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))
    from_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))

    next_node = relationship('PipelineNode', foreign_keys='PipelineLink.to_node_id', uselist=False)
    previous_node = relationship('PipelineNode', foreign_keys='PipelineLink.from_node_id', uselist=False)

    def __repr__(self, **kwargs) -> str:
        return super().__repr__(to_node=self.to_node_id, from_node=self.from_node_id, **kwargs)


INPUT_DIRNAME = 'input'
OUTPUT_DIRNAME = 'output'


class PipelineRun(IOPathMixin, Base):
    pipeline_id = Column(ForeignKey('pipeline.id', ondelete="CASCADE"))
    status = Column(String, default='Created')

    created_datetime = Column(DateTime, default=datetime.utcnow)
    finished_datetime = Column(DateTime)


class PipelineJob(IOPathMixin, TimestampMixin, Base):
    pipeline_run_id = Column(ForeignKey("pipeline_run.id", ondelete="CASCADE"))
    pipeline_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))
    status = Column(String)
    exit_code = Column(Integer)

    error = relationship('PipelineJobError', backref="job", uselist=False)


class PipelineJobError(Base):
    pipeline_job_id = Column(ForeignKey("pipeline_job.id", ondelete="CASCADE"))
    stderr = Column(String)
