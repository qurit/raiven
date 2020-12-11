import os

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from typing import List

from api import session
from api.schemas import user, destination
from api.models.destination import Destination
from api.models.user import User, testing
from api.auth import token_auth


router = APIRouter()


@router.get("/", response_model=List[destination.Destination])
def get_all_destinations(db: Session = Depends(session)):
    """ Get all application entities"""
    return db.query(Destination).all()


@router.post("/")
def create_destination(destination: destination.CreateDestination, db: Session = Depends(session)):
    """ Create a new application entity"""
    new_destination = Destination(
        host=destination.host, port=destination.port, full_name=destination.host + " " + str(destination.port))
    new_destination.save(db)
    return new_destination


@router.put("/user-destination")
def update_user_destination(destinations: user.blah, user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Update the user's application title"""
    print(destinations)
    db.query(testing).filter(
        testing.user_id == user.id).delete()
    user_destinations = destinations.destinations
    for dest in user_destinations:
        new_destination_user = testing(user_id=user.id,
                                               destination_id=dest.id)
        new_destination_user.save(db)
    return new_destination_user


# @router.get("/user-destination", response_model=List[destination.UserDestination])
# def get_user_destinations(user: User = Depends(token_auth), db: Session = Depends(session)):
#     """ Get the user's permitted application entities (to receive) """
#     return db.query(UserDestination).filter(UserDestination.user_id == user.id).all()
