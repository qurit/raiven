import os

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from typing import List

from api import session
from api.schemas import user, destination
from api.models.destination import Destination
from api.models.user import User, UserDestination
from api.auth import token_auth


router = APIRouter()


@router.get("/", response_model=List[destination.Destination])
def get_all_destinations(db: Session = Depends(session)):
    return db.query(Destination).all()


@router.post("/")
def create_destination(destination: destination.CreateDestination, db: Session = Depends(session)):
    new_destination = Destination(
        host=destination.host, port=destination.port, full_name=destination.host + " " + str(destination.port))
    new_destination.save(db)
    return new_destination


@router.put("/user-destination")
def update_user_destination(destination_ids: user.UserDestination, user: User = Depends(token_auth), db: Session = Depends(session)):
    print(destination_ids.destination_ids)
    print(user.id)
    db.query(UserDestination).filter(
        UserDestination.user_id == user.id).delete()
    for destination_id in destination_ids.destination_ids:
        new_destination_user = UserDestination(user_id=user.id,
                                               destination_id=destination_id)
        new_destination_user.save(db)

    return "ok"


@router.get("/user-destination", response_model=List[destination.UserDestination])
def get_user_destinations(user: User = Depends(token_auth), db: Session = Depends(session)):
    return db.query(UserDestination).filter(UserDestination.user_id == user.id).all()
