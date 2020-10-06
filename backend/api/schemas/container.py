from . import BaseModel, BaseORMModel


class ContainerCreate(BaseModel):
    user_id: int
    name: str
    description: str
    dockerfile_path: str
    is_input_container: bool
    is_output_container: bool


class Container(ContainerCreate, BaseORMModel):
    user_id: int
