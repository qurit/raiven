from . import BaseModel, BaseORMModel
from typing import Optional
from .user import User


class ContainerCreate(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    dockerfile_path: Optional[str] = None
    is_input_container: Optional[bool] = False
    is_output_container: Optional[bool] = False
    is_shared: Optional[bool] = False
    filename: Optional[str] = None


class Container(ContainerCreate, BaseORMModel):
    user_id: int
    user: User
