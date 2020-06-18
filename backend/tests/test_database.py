from tests import app, mongo, config

def test_index():
    print(type(mongo))
    assert mongo.db.HOST == True
