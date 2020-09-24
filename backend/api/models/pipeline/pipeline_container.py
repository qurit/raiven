from sqlalchemy import *
from sqlalchemy.orm import relationship

from .. import Base


class Container(Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)
    dockerfile_path = Column(String)


class Pipeline(Base):
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    name = Column(String)


class PipelineStep(Base):
    pipeline_id = Column(ForeignKey("pipeline.id", ondelete="CASCADE"))
    container_id = Column(ForeignKey("container.id"))
    next_pipeline_step_id = Column(ForeignKey("pipeline_step.id"))

    # next = relationship("PipelineStep", backref="previous")






