""" Config """
from config import init_config
config = init_config()

# if not config.IS_WORKER:
import eventlet
eventlet.monkey_patch()

""" Setting Up Background Tasks """
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import CurrentMessage
broker = RabbitmqBroker(host=config.RABBITMQ_HOST, middleware=[CurrentMessage()])
dramatiq.set_broker(broker)

""" Setting Up Docker """
from docker import DockerClient
docker = DockerClient(config.DOCKER_URI)

""" Setting Up Flask """
from flask import Flask, render_template
from flask_restx import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False
CORS(app, resources={r'/*': {'origins': '*'}})

""" Setting up Database"""
from api.database import init_db

db = SQLAlchemy(app)
init_db(db)

""" Setting up websockets """
from api.sockets import init_socketio

socketio = init_socketio()
api = Api(app)

""" Importing Routes """
from api import routes
from api.sockets import test


@app.route('/test')
def test():
    return render_template('index.html', async_mode=config.ASYNC_MODE)
