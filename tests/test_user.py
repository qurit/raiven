import os
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from api import app
from api.schemas.pipeline import UserCreate

client = TestClient(app)


def get_test_user():
    if len(users := test_get_users()):
        return users[0]
    else:
        return test_add_user()


def test_get_users() -> list:
    response = client.get('/user/')
    assert response.status_code == 200
    data = response.json()

    assert type(data) is list
    return data


DEFAULT_USER = UserCreate(
    username='joeBlow420',
    name='Joe Blow',
    title='Tester',
    department='IT',
    company='Google'
)


# def test_add_user(user: UserCreate = DEFAULT_USER) -> dict:
#     response = client.post('/user/', json=user.dict())
#
#     assert response.status_code == 200
#     data = response.json()
#
#     assert data['username'] == user.username
#     assert data['name'] == user.name
#     assert data['title'] == user.title
#     assert data['department'] == user.department
#     assert data['company'] == user.company
#
#     all_users = test_get_users()
#     assert len([u for u in all_users if u.id == data['id']]) == 1, "Newly created user is not in the list of all users"
#
#     return data




