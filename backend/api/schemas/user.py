from typing import Optional

from . import BaseORMModel, BaseModel


class UserLocalCreate(BaseModel):
    username: str
    name: str
    password: str


class User(BaseORMModel):
    username: str
    name: str
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

