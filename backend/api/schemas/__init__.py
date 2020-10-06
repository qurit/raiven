from ._base import BaseModel, BaseORMModel
from . import pipeline
from . import container


class ApplicationEntityCreate(BaseModel):
    title: str


class ApplicationEntity(ApplicationEntityCreate, BaseORMModel):
    pass

