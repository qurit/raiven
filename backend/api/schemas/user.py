from typing import Optional

from . import BaseORMModel, BaseModel


class UserCreate(BaseModel):
    username: str
    name: str
    title: Optional[str]
    department: Optional[str]
    company: Optional[str]


class User(UserCreate, BaseORMModel):
    is_admin: bool
