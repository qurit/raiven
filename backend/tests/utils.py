from tests import models, config, schemas, TEST_USER, client


def create_local_user(name, username, password) -> schemas.user.User:
    user_to_create = schemas.user.UserLocalCreate(name=name, username=username, password=password)
    response = client.post('/user/', json=user_to_create.dict())
    data = response.json()

    assert response.status_code == 200
    assert data['username'] == user_to_create.username
    assert data['name'] == user_to_create.name
    assert not data['is_admin']

    return schemas.user.User(**data)


def get_test_user(db) -> models.user.User:
    assert (user := db.query(models.user.User).filter_by(username=TEST_USER.username).first())

    return user
