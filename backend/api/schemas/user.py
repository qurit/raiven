from typing import Optional
from datetime import datetime

from . import BaseORMModel, BaseModel


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
    first_seen: datetime
    last_seen: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

