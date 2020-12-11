from typing import Optional, List
from datetime import datetime

from . import BaseORMModel, BaseModel
from .destination import Destination


class UserLocalCreate(BaseModel):
    username: str
    name: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "testuser",
                "name": "Mr. Testing",
                "password": "password"
            }
        }


class User(BaseORMModel):
    username: str
    name: str
    is_admin: bool
    ae_title: Optional[str]
    first_seen: datetime
    last_seen: datetime


class UserEdit(BaseModel):
    ae_title: str


class blah(BaseModel):
    destinations: Optional[List[Destination]]


class test(BaseORMModel):
    destination: Destination


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
