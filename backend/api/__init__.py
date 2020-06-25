import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import CurrentMessage
dramatiq.set_broker(RabbitmqBroker(host="rabbitmq", middleware=[CurrentMessage()]))

from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_pymongo import PyMongo
from flask_cors import CORS

# import dicom.utils
# from dicom.echo import echo
from config import BaseConfig

config = BaseConfig()

app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False
CORS(app, resources={r'/*': {'origins': '*'}})


mongo = PyMongo(app)
db = mongo.db

from api.encoders import jsonify
from api.routes.modalities import api as ns_api
api = Api(app)
api.add_namespace(ns_api)

from api.tasks.hello import count_words


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        msg = count_words.send()
        db.jobs.insert_one({'pid': msg.message_id, 'status': 'Queued', 'info': str(count_words)})
        return {'hello': 'world'}


