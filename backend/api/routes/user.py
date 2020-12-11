from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException

from api import session, config
from api.models.user import User, UserLocal, UserDestination
from api.schemas.user import User as UserSchema, UserLocalCreate, UserEdit, blah, test
from api.auth import token_auth

router = APIRouter()



@router.get("/", response_model=List[UserSchema], dependencies=[Depends(token_auth)])
def get_all_users(db: Session = Depends(session)):
    """
    Get all users.
    """
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
    """
    Get current user
    """
    return user


@router.put("/{user_id}")
def edit_user_settings(user_id: int, new_info: UserEdit, user: User = Depends(token_auth), db: Session = Depends(session)):
    """
    Edit user settings
    """
    if user.id != user_id and not user.is_admin:
        return HTTPException(403, 'Unauthorized')

    if not (user_to_edit := db.query(User).get(user_id)):
        return HTTPException(401, 'User does not exist')

    user_to_edit.ae_title = new_info.ae_title
    user_to_edit.save(db)
    return user_to_edit


@router.put("/user-destination")
def test_put(user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Update the user's application title"""
    return "ok"


@router.get("/ae-title", response_model=List[test])
def get_put(user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Get the user's permitted application entities (to receive) """
    print(user)
    return db.query(UserDestination).filter(UserDestination.user_id == user.id).all()
