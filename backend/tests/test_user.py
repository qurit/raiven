import os

from api.models.user import User
from api.schemas.user import UserCreate

from . import client, testing_session


def test_get_users() -> list:
    response = client.get('/user/')
    assert response.status_code == 200
    data = response.json()
    print("ALL USERS", data)

    assert type(data) is list
    return data


DEFAULT_USER = UserCreate(
    username='joeBlow420',
    name='Joe Blow',
    title='Tester',
    department='IT',
    company='Google'
)


def test_add_user(user: UserCreate = DEFAULT_USER) -> dict:
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
        assert data['title'] == user.title
        assert data['department'] == user.department
        assert data['company'] == user.company

        all_users = test_get_users()
        assert len([u for u in all_users if u.id == data['id']]) == 1, "Newly created user is not in the list of all users"

    return data




