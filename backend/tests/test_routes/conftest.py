import pytest

from tests import client, TEST_USER, models, config


@pytest.fixture(scope="module")
def authorization_header():
    response = client.post('/auth/token', data={'username': TEST_USER.username, 'password': TEST_USER.password})
    assert response.status_code == 200

    return {'Authorization': f'Bearer {response.json()["access_token"]}'}


@pytest.fixture(scope='function')
def custom_serializer():
    models.user.User._set_serializer('my key', 0)

    yield models.user.User

    models.user.User._set_serializer(config.SECRET_KEY, config.TOKEN_TTL)



