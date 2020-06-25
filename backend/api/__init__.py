import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import CurrentMessage
dramatiq.set_broker(RabbitmqBroker(host="rabbitmq", middleware=[CurrentMessage()]))

from flask import Flask
from flask_restx import Resource, Api, fields
from flask_pymongo import PyMongo
from flask_cors import CORS

from config import BaseConfig
config = BaseConfig()

app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False
CORS(app, resources={r'/*': {'origins': '*'}})

mongo = PyMongo(app)
db = mongo.db

from api.routes.modalities import api as ns_api
from api.routes.jobs import api as ns_jobs

api = Api(app)
api.add_namespace(ns_api)
api.add_namespace(ns_jobs)



