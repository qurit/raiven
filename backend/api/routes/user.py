from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException

from api import session, config
from api.models.user import User
from api.schemas.user import User as UserSchema, UserCreate as UserCreateSchema

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(session)):
    users = db.query(User).all()
    print(users)

    return users


@router.post("/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(session)):
    """
    Allows the creation of a user. This route should exist purely for testing purposes. User creation should be done by LDAP.
    """
    print(config.SQLALCHEMY_DATABASE_URI)

    try:
        user = User(**user.dict())
        user.save(db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='User already exists')
    else:
        return user
