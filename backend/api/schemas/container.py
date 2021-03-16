from . import BaseModel, BaseORMModel
from typing import Optional, List, Any
from .user import User


class ContainerStats(BaseModel):
    container_counts: int


class ContainerCreate(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    dockerfile_path: Optional[str] = None
    is_input_container: Optional[bool] = False
    is_output_container: Optional[bool] = False
    is_shared: Optional[bool] = False
    filename: Optional[str] = None


class Tag(BaseORMModel):
    tag_name: str


class ContainerTag(BaseModel):
    container_id: int
    tag_id: int
    tag: str


class Container(ContainerCreate, BaseORMModel):
    user_id: int
    user: User
    tags: Optional[List[Any]]
