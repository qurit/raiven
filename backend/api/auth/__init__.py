from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from api import session
from api.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


def token_auth(token: str = Depends(oauth2_scheme), db: type(session) = Depends(session)):
    if not (user := User.verify_token(token, db)):
        return HTTPException(401, "Invalid token")
    else:
        return user
