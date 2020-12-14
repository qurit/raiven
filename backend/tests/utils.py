from tests import models, config, TEST_USER


def get_test_user(db) -> models.user.User:
    assert (user := db.query(models.user.User).filter_by(username=TEST_USER.username).first())

    return user
