from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException

from api import session, config
from api.models.user import User, UserLocal
from api.schemas.user import User as UserSchema, UserLocalCreate
from api.auth import token_auth

router = APIRouter()


@router.get("/", response_model=List[UserSchema], dependencies=[Depends(token_auth)])
def get_all_users(db: Session = Depends(session)):
    return db.query(User).all()


@router.post("/", response_model=UserSchema)
def create_local_user(user_schema: UserLocalCreate, db: Session = Depends(session)):
    """
    Allows the creation of a local user.
    """

    try:
        user = User(username=user_schema.username, name=user_schema.name)
        user.save(db)

        UserLocal(id=user.id, password=user_schema.password).save(db)

    except IntegrityError:
        raise HTTPException(status_code=400, detail='User already exists')
    else:
        return user


@router.get("/me", response_model=UserSchema)
def get_the_current_user(user: User = Depends(token_auth)):
    return user

