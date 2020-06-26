from os import environ

LOCALHOST = '127.0.0.1'


# noinspection PyPep8Naming
class BaseConfig(object):
    HOST = LOCALHOST
    PORT = 5000

    # LDAP CONFIG
    LDAP_HOST = '10.9.2.37'
    LDAP_PORT = 389
    LDAP_USE_SSL = False
    LDAP_USERNAME_BASE = 'CRC\\'
    LDAP_BASE_DN = 'DC=BCCRC,DC=CA'
    LDAP_TEST_USR = 'crcldapviewer'
    LDAP_TEST_PW = 'LD@P2020pw!'

    # DB SETTINGS
    MONGO_USER = 'picom_admin'
    MONGO_PASSWORD = 'password'
    MONGO_HOST = LOCALHOST
    MONGO_PORT = 27017
    MONGO_DB = 'picom'

    # AUTH
    SECRET_KEY = 'replace_me!'
    AUTH_ENABLED = True
    BASIC_AUTH_FORCE = True
    TOKEN_TTL = 3600 * 24 * 7  # 12 hours before the token expires

    # SOCKET IO
    WEB_SOCKETS_ENABLED = True

    # PROCESSING QUEUE
    RABBITMQ_HOST = LOCALHOST
    RABBITMQ_PORT = 5672
    IS_WORKER = False
    ASYNC_MODE = 'eventlet'

    # Docker
    DOCKER_URI = 'tcp://localhost:2375'

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
