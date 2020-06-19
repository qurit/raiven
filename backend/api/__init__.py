from flask import Flask
from flask_restplus import Resource, Api
from flask_pymongo import PyMongo

from config import BaseConfig
config = BaseConfig()

app = Flask(__name__)
app.config.from_object(config)

api = Api(app)
mongo = PyMongo(app)
db = mongo.db


@api.route('/hello')
class HelloWorld(Resource):

    def get(self):
        mongo.db.users.insert_one({ 'test': 0, 'AET': 'MIT'})
        return {'hello': 'world'}


if __name__ == '__main__':
    app.run(debug=True)
