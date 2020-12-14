from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException

from api import session, config
from api.models.user import User, UserLocal, UserDestination
from api.schemas.user import User as UserSchema, UserLocalCreate, UserEdit, PermittedApplicationEntities, ApplicationEntity
from api.auth import token_auth

router = APIRouter()



@router.get("/", response_model=List[UserSchema], dependencies=[Depends(token_auth)])
def get_all_users(db: Session = Depends(session)):
    """ Get all users."""
    return db.query(User).all()


@router.post("/", response_model=UserSchema)
def create_local_user(user_schema: UserLocalCreate, db: Session = Depends(session)):
    """  Allows the creation of a local user. """

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
    """ Get current user """
    return user


@router.put("/{user_id}")
def edit_user_settings(user_id: int, new_info: UserEdit, user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Edit user settings """
    if user.id != user_id and not user.is_admin:
        return HTTPException(403, 'Unauthorized')

    if not (user_to_edit := db.query(User).get(user_id)):
        return HTTPException(401, 'User does not exist')

    user_to_edit.ae_title = new_info.ae_title
    user_to_edit.save(db)
    return user_to_edit

@router.post("/permitted-ae")
def update_permitted_ae(destinations: PermittedApplicationEntities, user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Update the user's application title"""
    db.query(UserDestination).filter(
        UserDestination.user_id == user.id).delete()
    user_destinations = destinations.destinations
    for dest in user_destinations:
        new_destination_user = UserDestination(user_id=user.id, destination_id=dest.id)
        new_destination_user.save(db)
    return new_destination_user


@router.get("/permitted-ae", response_model=List[ApplicationEntity])
def get_permitted_ae(user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Get the user's permitted application entities (to receive) """
    return db.query(UserDestination).filter(UserDestination.user_id == user.id).all()
