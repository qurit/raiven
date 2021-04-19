from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import session
from api.auth import admin_auth
from api.auth import token_auth
from api.models.user import User, UserLocal, UserLDAP
from api.schemas.user import User as UserSchema, UserLDAPSchema, UserLocalCreate, UserEdit, PermittedApplicationEntities, \
    ApplicationEntity

router = APIRouter()


@router.put("/modify-access/{user_id}", dependencies=[Depends(admin_auth)])
def modify_user_access(user_id: int, db: Session = Depends(session)):
    """ Change the user's access permissions """
    user = db.query(User).get(user_id)
    user.access_allowed = not user.access_allowed
    user.save(db)
    return user


@router.put("/modify-role/{user_id}", dependencies=[Depends(admin_auth)])
def modify_user_role(user_id: int, db: Session = Depends(session)):
    """ Change the user's role """
    user = db.query(User).get(user_id)
    user.is_admin = not user.is_admin
    user.save(db)
    return user


@router.get("/", response_model=List[UserSchema], dependencies=[Depends(admin_auth)])
def get_all_users(db: Session = Depends(session)):
    """ Gets all the users in the database. Only Admins are allowed to access this endpoint."""

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


@router.put("/{user_id}", response_model=UserSchema)
def edit_user_settings(user_id: int, new_info: UserEdit, user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Edit user settings """
    if user.id != user_id and not user.is_admin:
        return HTTPException(403, 'Unauthorized')

    if not (user_to_edit := db.query(User).get(user_id)):
        return HTTPException(401, 'User does not exist')

    user_to_edit.ae_title = new_info.ae_title
    user_to_edit.save(db)
    return user_to_edit

# TODO FIX THIS
# @router.post("/permitted-ae", response_model=List[Destination])
# def update_permitted_ae(destinations: PermittedApplicationEntities, user: User = Depends(token_auth), db: Session = Depends(session)):
#     """ Update the user's application title"""
#     db.query(UserDestination).filter(
#         UserDestination.user_id == user.id).delete()
#     user_destinations = destinations.destinations
#     for dest in user_destinations:
#         new_destination_user = UserDestination(user_id=user.id, destination_id=dest.id)
#         new_destination_user.save(db)
#     return user_destinations


@router.get("/permitted-ae", response_model=List[ApplicationEntity])
def get_permitted_ae(user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Get the user's permitted application entities (to receive) """
    # return db.query(DicomNode).filter(UserDestination.user_id == user.id).all()
    return []
