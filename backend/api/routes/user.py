from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from api import session
from api.models.user import User
from api.schemas import pipeline as schemas

router = APIRouter()

# TODO: delete this stuff, need this to get it working with the containe stuff


@router.get("/")
def get_all_users(db: Session = Depends(session)):
    print("the users")
    return db.query(User).all()


@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(session)):
    print(user)
    return User(**user.dict()).save(db)
