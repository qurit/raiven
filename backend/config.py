from os import environ

LOCALHOST = '127.0.0.1'


# noinspection PyPep8Naming
class BaseConfig(object):
    HOST = LOCALHOST
    PORT = 5000

    SECRET_KEY = 'replace_me!'

    # DB SETTINGS
    MONGO_USER = 'picom_admin'
    MONGO_PASSWORD = 'password'
    MONGO_HOST = LOCALHOST
    MONGO_PORT = 27017
    MONGO_DB = 'picom'

    # SOCKET IO
    WEB_SOCKETS_ENABLED = True

    # PROCESSING QUEUE
    RABBITMQ_HOST = LOCALHOST
    RABBITMQ_PORT = 5672
    IS_WORKER = False

    ASYNC_MODE = 'eventlet'

    @property
    def MONGO_URI(self):
        return f'mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}'

    @property
    def RABBITMQ_URI(self):
        return f'amqp://{self.RABBITMQ_HOST}'


class DockerConfig(BaseConfig):
    HOST = '0.0.0.0'
    MONGO_HOST = 'mongo'
    RABBITMQ_HOST = 'rabbitmq'


class WorkerConfig(DockerConfig):
    IS_WORKER = True


def init_config():
    env = environ.get('FLASK_ENV')
    configs = {
        'docker': DockerConfig,
        'worker': WorkerConfig
    }

    config = configs[env] if env in configs.keys() else BaseConfig
    return config()
