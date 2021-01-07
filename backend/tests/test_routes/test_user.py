import os

from api.models.user import User
from api.schemas.user import UserLocalCreate

from tests import client, testing_session, utils


def test_get_users() -> list:
    response = client.get('/user/')
    assert response.status_code == 401


def test_add_user():
    test_user = UserLocalCreate(
        username='joeSmith',
        name='Joe Smith',
        password='password',
    )

    with testing_session() as db:
        if user := db.query(User).filter_by(username=test_user.username).first():
            user.delete(db)
            db.commit()

    utils.create_local_user(**test_user.dict())









