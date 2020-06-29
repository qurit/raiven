import flask_pymongo

from tests import app, mongo, config, db


def test_mongo_config():
    assert type(mongo) is flask_pymongo.PyMongo
    assert type(mongo.cx) is flask_pymongo.MongoClient

    if config.MONGO_HOST != '127.0.0.1':
        assert mongo.cx.HOST == config.MONGO_HOST
    assert mongo.cx.PORT == config.MONGO_PORT


def test_db_config():
    assert type(mongo.db) is flask_pymongo.wrappers.Database
    assert type(db) is flask_pymongo.wrappers.Database

    assert mongo.db.name == config.MONGO_DB
    assert db.name == config.MONGO_DB
