from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api import session, config
from api.models.user import User, UserLocal
from api.schemas.user import User as UserSchema, UserLocalCreate, Token

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(session)):
    users = db.query(User).all()
    print(users)

    return users


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


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(session)):
    user = User.query(db).filter_by(username=form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if ldap := user.ldap_user:
        #TODO: implement ldap authentication
        pass
    elif (local := user.local_user) and not local.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return Token(token=user.generate_token())

