import dramatiq
import docker as _docker
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from api import config

docker = _docker.from_env()
dramatiq.set_broker(RabbitmqBroker(host=config.RABBITMQ_HOST))