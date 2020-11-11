import docker as _docker
import dramatiq
import socketio
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from api import config

docker = _docker.from_env()
dramatiq.set_broker(RabbitmqBroker(host=config.RABBITMQ_HOST))

external_sio = socketio.AsyncAioPikaManager()
