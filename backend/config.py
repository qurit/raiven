from os import environ


# noinspection PyPep8Naming
class BaseConfig(object):
    HOST = '127.0.0.1'
    PORT = 5000

    SECRET_KEY = 'replace_me!'

    # DB SETTINGS
    MONGO_USER = 'picom_admin'
    MONGO_PASSWORD = 'password'
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_DB = 'picom'

    # SOCKET IO
    WEB_SOCKETS_ENABLED = False

    # PROCESSING QUEUE
    RABBITMQ_HOST = 'localhost'

    @property
    def MONGO_URI(self):
        return f'mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}'


class DockerConfig(BaseConfig):
    HOST = '0.0.0.0'
    MONGO_HOST = 'mongo'
    RABBITMQ_HOST = 'rabbitmq'


def init_config():
    env = environ.get('FLASK_ENV')
    configs = {
        'docker': DockerConfig,
    }

    config = configs[env] if env in configs.keys() else BaseConfig
    return config()
