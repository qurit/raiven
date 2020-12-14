import pytest
from sqlalchemy_utils import drop_database, create_database, database_exists

from tests import testing_session, models, TEST_USER
from api import engine, scripts


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    assert 'test' in str(url := engine.url)

    if database_exists(url):
        drop_database(url)

    create_database(engine.url)
    models.Base.metadata.create_all(bind=engine)
    scripts.run_startup_scripts()

    with testing_session() as db:
        models.user.User(username=TEST_USER.username, name=TEST_USER.name).save(db)
        db.commit()

    yield


@pytest.fixture
def db():
    with testing_session() as db:
        yield db


