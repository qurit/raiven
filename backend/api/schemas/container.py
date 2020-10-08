from . import BaseModel, BaseORMModel
from typing import Optional


class ContainerCreate(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    dockerfile_path: Optional[str] = None
    is_input_container: bool
    is_output_container: bool


class Container(ContainerCreate, BaseORMModel):
    user_id: int
