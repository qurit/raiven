from ._base import BaseModel, BaseORMModel
from . import pipeline


class ApplicationEntityCreate(BaseModel):
    title: str


class ApplicationEntity(ApplicationEntityCreate, BaseORMModel):
    pass


# class ContainerCreate(BaseModel):
#     name: str
#     dockerfile_path: str


# class Container(ContainerCreate, BaseORMModel):
#     user_id: str
#     pass

# TODO: to delete, put this here for now to get container working
class ContainerCreate(BaseModel):
    user_id: int
    name: str
    dockerfile_path: str


class Container(ContainerCreate, BaseORMModel):
    user_id: int
    pass
