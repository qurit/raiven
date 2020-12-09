from . import BaseModel, BaseORMModel
from typing import Optional
from .user import User


class ContainerCreate(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    dockerfile_path: Optional[str] = None
    is_input_container: bool
    is_output_container: bool
    is_shared: bool
    filename: str


class Container(ContainerCreate, BaseORMModel):
    user_id: int
    user: User
