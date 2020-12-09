from tests import client
from tests.test_routes.test_user import create_local_user


def test_login():
    username = 'test_login'
    password = 'test_password'

    user = create_local_user('test', username, password)
    assert user

    response = client.post('/auth/token', data={'username': user.username, 'password': password})
    assert response.status_code == 200

    data = response.json()
    assert 'access_token' in data and type(data['access_token']) is str


def test_login_failure():
    username = 'test_failure'
    password = 'my_password'
    user = create_local_user('test', username, password)

    response = client.post('/auth/token', data={'username': user.username, 'password': password})
    assert response.status_code == 200

    response = client.post('/auth/token', data={'username': user.username, 'password': password+'sds'})
    assert response.status_code == 401

    response = client.post('/auth/token', data={'username': user.username, 'password': password[:-2]})
    assert response.status_code == 401

    response = client.post('/auth/token', data={'username': user.username.replace('_', ''), 'password': password})
    assert response.status_code == 401


def test_login_empty():
    response = client.post('/auth/token', data={'username': '', 'password': ''})
    assert response.status_code in [401, 422]


def test_login_no_body():
    response = client.post('/auth/token')
    assert response.status_code == 422


