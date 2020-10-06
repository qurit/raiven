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

class ContainerCreate(BaseModel):
    user_id: int
    name: str
    description: str
    dockerfile_path: str
    is_input_container: bool
    is_output_container: bool
    dockerfile: str


class Container(ContainerCreate, BaseORMModel):
    user_id: int
    pass
