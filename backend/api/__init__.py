from config import init_config
config = init_config()

# if not config.IS_WORKER:
import eventlet
eventlet.monkey_patch()

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import CurrentMessage

print('SETTING BROKER')
broker = RabbitmqBroker(host=config.RABBITMQ_HOST, middleware=[CurrentMessage()])
dramatiq.set_broker(broker)

from flask import Flask, render_template
from flask_restx import Api
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False
CORS(app, resources={r'/*': {'origins': '*'}})

mongo = PyMongo(app)
db = mongo.db

from docker import DockerClient
docker = DockerClient(config.DOCKER_URI)

from api.sockets import init_socketio

socketio = init_socketio()
api = Api(app)

from api import routes
from api.sockets import test


@app.route('/test')
def test():
    return render_template('index.html', async_mode=config.ASYNC_MODE)
