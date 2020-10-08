from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from api import session
from api.models.user import User
from api.schemas.user import User as UserSchema, UserCreate as UserCreateSchema

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(session)):
    return db.query(User).all()


@router.post("/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(session)):
    """
    Allows the creation of a user. This route should exist purely for testing purposes. User creation should be done by LDAP.
    """
    return User(**user.dict()).save(db)
