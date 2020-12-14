import pytest

from tests import client, TEST_USER


@pytest.fixture(scope="module")
def authorization_header():
    response = client.post('/auth/token', data={'username': TEST_USER.username, 'password': TEST_USER.password})
    assert response.status_code == 200

    return {'Authorization': f'Bearer {response.json()["access_token"]}'}

