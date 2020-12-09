import docker as _docker
import dramatiq
import socketio

from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.brokers.stub import StubBroker

from api import config

docker = _docker.from_env()
broker = StubBroker() if config.UNIT_TESTING else RabbitmqBroker(host=config.RABBITMQ_HOST)
dramatiq.set_broker(broker)
external_sio = socketio.AsyncAioPikaManager(write_only=True)