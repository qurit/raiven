import os

from api.models.user import User
from api.schemas.user import UserLocalCreate

from . import client, testing_session


def test_get_users() -> list:
    response = client.get('/user/')
    assert response.status_code == 401


DEFAULT_USER = UserLocalCreate(
    username='joeBlow420',
    name='Joe Blow',
    password='password',
)


def test_add_user(user: UserLocalCreate = DEFAULT_USER) -> dict:

    with testing_session() as db:
        exists = db.query(User).filter_by(username=user.username).first() is not None

    response = client.post('/user/', json=user.dict())
    data = response.json()

    if exists:
        assert response.status_code != 200
    else:
        assert response.status_code == 200
        assert data['username'] == user.username
        assert data['name'] == user.name

        all_users = test_get_users()

    return data






