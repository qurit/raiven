from tests import models, config


def get_test_user(db) -> models.user.User:
    assert (user := db.query(models.user.User).filter_by(username=config.INTERNAL_USERNAME).first())

    return user
