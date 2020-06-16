from flask import Flask
from flask_restplus import Resource, Api
from flask_pymongo import PyMongo

from api.config import BaseConfig
config = BaseConfig()

app = Flask(__name__)
app.config.from_object(config)

api = Api(app)
mongo = PyMongo(app)


@api.route('/hello')
class HelloWorld(Resource):

    def get(self):
        return {'hello': 'world'}


if __name__ == '__main__':
    app.run(debug=True)
