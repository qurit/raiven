import os

from api.models.user import User
from api.schemas.user import UserLocalCreate, User as UserSchema

from tests import client, testing_session


def create_local_user(name, username, password) -> UserSchema:
    user_to_create = UserLocalCreate(name=name, username=username, password=password)
    response = client.post('/user/', json=user_to_create.dict())
    data = response.json()

    assert response.status_code == 200
    assert data['username'] == user_to_create.username
    assert data['name'] == user_to_create.name
    assert not data['is_admin']

    return UserSchema(**data)


def test_get_users() -> list:
    response = client.get('/user/')
    assert response.status_code == 401


def test_add_user():
    test_user = UserLocalCreate(
        username='joeBlow420',
        name='Joe Blow',
        password='password',
    )

    with testing_session() as db:
        if user := db.query(User).filter_by(username=test_user.username).first():
            user.delete(db)
            db.commit()

    create_local_user(**test_user.dict())








