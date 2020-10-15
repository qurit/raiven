import os
from sqlalchemy import *
from sqlalchemy.orm import relationship

from api import config
from . import Base, PathMixin, NestedPathMixin


class Pipeline(Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)

    nodes = relationship("PipelineNode", backref="pipeline")
    links = relationship("PipelineLink", backref="pipeline")

    # TODO: This query can be optimized by joins
    def get_starting_nodes(self):
        return [n for n in self.nodes if n.is_root_node()]


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


class PipelineRun(Base):
    pass


INPUT_DIRNAME = 'input'
OUTPUT_DIRNAME = 'output'


class PipelineJob(PathMixin, Base):
    pipeline_run_id = Column(ForeignKey("pipeline_run.id", ondelete="CASCADE"))
    pipeline_node_id = Column(ForeignKey("pipeline_node.id", ondelete="CASCADE"))
    status = Column(String)
    exit_code = Column(Integer)
    # TODO: Add Error logging (seperate table)

    input_path = Column(String)
    output_path = Column(String)

    error = relationship('PipelineJobError', backref="job", uselist=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Making folders
        abs_path = self.get_abs_path()
        [os.makedirs(p) for dirname in [INPUT_DIRNAME, OUTPUT_DIRNAME] if not os.path.exists(p := os.path.join(abs_path, dirname))]

        # Saving Path info
        rel_path = self.get_path()
        self.input_path = os.path.join(rel_path, INPUT_DIRNAME)
        self.output_path = os.path.join(rel_path, OUTPUT_DIRNAME)
        super().save(*args, **kwargs)


class PipelineJobError(Base):
    pipeline_job_id = Column(ForeignKey("pipeline_job.id", ondelete="CASCADE"))
    stderr = Column(String)
