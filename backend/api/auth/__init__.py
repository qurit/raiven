from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from api import session
from api.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def token_auth(token: str = Depends(oauth2_scheme), db: type(session) = Depends(session)):
    if not (user := User.verify_token(token, db)):
        raise HTTPException(401, "Invalid token")
    else:
        return user


def socket_auth(token):
    return User.verify_token(token)


def admin_auth(token: str = Depends(oauth2_scheme), db: type(session) = Depends(session)):
    user = token_auth(token, db)

    if type(user) is User and not user.is_admin:
        raise HTTPException(403, "Unauthorized")

    return user
