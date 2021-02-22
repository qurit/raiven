from . import BaseModel, BaseORMModel
from typing import Optional, List
from .user import User
from api.models import container


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


class ContainerTags(BaseModel):
    # To create the list of tags associated with the container
    tag_ids: List[int]


class Tag(BaseModel):
    # To create a new Tag in the Tag db
    tag_name: str


class ContainerTag(BaseModel):
    # To associate the tags with the appropriate container
    container_id: int
    tag_id: int

    tags: List[Tag]


class Container(ContainerCreate, BaseORMModel):
    user_id: int
    user: User
