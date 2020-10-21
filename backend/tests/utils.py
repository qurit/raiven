from api.schemas.user import User as UserSchema

from .test_user import test_add_user, test_get_users


def get_test_user() -> UserSchema:
    if len(users := test_get_users()):
        return UserSchema(**users[0])
    else:
        return UserSchema(**test_add_user())
