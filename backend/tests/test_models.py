from flask_restx import Model
from flask_pymongo import wrappers

from tests import app, mongo, config, db


from api import models


# noinspection PyProtectedMember
def test_base():
    base = models.BaseModel()

    # Making sure api models are correct
    assert type(base.model()) is Model
    assert type(base.list_model()) is Model

    assert base, 'Should not be None'
    assert not base.get_id()
    assert not vars(base), 'Model should not have any vars'

    # Object ID's
    oid = 'My object id'
    base = models.BaseModel(_id=oid)
    assert base._id == oid, "Object ID Should be stored"
    assert len(vars(base)) == 1, 'Model should have exactly one var'
    assert vars(base)['_id'] == oid, 'Object id should be in the model vars'
    assert base.get_id() == oid

    base = models.BaseModel(_id=oid, test=4, yes='no')
    assert base.test == 4, "Object ID Should be stored"
    assert len(vars(base)) == 3, 'Model should have exactly 3 vars'
    assert base.get_id() == oid


def collection(model=None):
    def decorator(func):
        assert type(model.__collection__) is wrappers.Collection
        assert model.__collection__.name == f'{model.__name__.lower()}s'
        return func
    return decorator


@collection(model=models.User)
def test_user():
    user = models.User(username='Adam')
    assert user, 'Should not be None'
    assert not user.get_id()
    assert not user.in_db()

    user.insert()
    assert user.get_id()
    assert user.in_db()
    assert models.User.__collection__.find_one({'_id': user.get_id()})

    user.username = "Joe"
    user.company = "Google"
    user.update()
    assert models.User.__collection__.find_one({'_id': user.get_id(), 'username': 'Joe', 'company': 'Google'})

    assert user.delete()
    assert not models.User.__collection__.find_one({'_id': user.get_id()})



