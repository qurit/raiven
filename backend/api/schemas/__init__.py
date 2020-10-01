from ._base import BaseModel, BaseORMModel
from . import pipeline


class ApplicationEntityCreate(BaseModel):
    title: str


class ApplicationEntity(ApplicationEntityCreate, BaseORMModel):
    pass


class ContainerCreate(BaseModel):
    name: str
    dockerfile_path: str


class Container(ContainerCreate, BaseORMModel):
    user_id: str
    pass
