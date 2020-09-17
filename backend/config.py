import os

LOCALHOST = '127.0.0.1'


# noinspection PyPep8Naming
class BaseConfig(object):
    HOST = LOCALHOST
    PORT = 5000

    # AUTH
    SECRET_KEY = 'replace_me!'
    AUTH_ENABLED = False
    BASIC_AUTH_FORCE = True
    TOKEN_TTL = 3600 * 12  # 12 hours before the token expires

    # LDAP CONFIG
    LDAP_HOST = '10.9.2.37'
    LDAP_PORT = 389
    LDAP_USE_SSL = False
    LDAP_USERNAME_BASE = 'CRC\\'
    LDAP_BASE_DN = 'DC=BCCRC,DC=CA'
    LDAP_TEST_USR = 'crcldapviewer'
    LDAP_TEST_PW = 'LD@P2020pw!'

    # DB
    MIGRATION_DIR = os.path.join(os.getcwd(), 'migrations')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_HOST = 'db.mit.bccrc.ca'
    POSTGRES_USER = 'biodi'
    POSTGRES_PW = 'bccrcbiodi'
    POSTGRES_DB = 'biodi'

    # SOCKET IO
    WEB_SOCKETS_ENABLED = True

    # PROCESSING QUEUE
    RABBITMQ_HOST = LOCALHOST
    RABBITMQ_PORT = 5672
    IS_WORKER = False
    ASYNC_MODE = 'eventlet'

    # Docker
    DOCKER_URI = 'tcp://127.0.0.1:2375'

    @property
    def POSTGRES_URI(self):
        return f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PW}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}'

    @property
    def RABBITMQ_URI(self):
        return f'amqp://{self.RABBITMQ_HOST}'


class DockerConfig(BaseConfig):
    HOST = '0.0.0.0'
    MONGO_HOST = 'picom_mongo'
    RABBITMQ_HOST = 'picom_rabbit'
    DOCKER_URI = 'unix://var/run/docker.sock'


class WorkerConfig(DockerConfig):
    IS_WORKER = True


def init_config():
    env = os.environ.get('FLASK_ENV')
    configs = {
        'docker': DockerConfig,
        'worker': WorkerConfig
    }

    # Setting config type
    config = configs[env] if env in configs.keys() else BaseConfig

    # Allows the configuration of all variables from environment variables
    for env_var in os.environ.keys():
        if env_var in vars(config) and not env_var.startswith('__'):
            print('SETTING VAR', env_var, os.environ[env_var])
            setattr(config, env_var, os.environ[env_var])

    return config()
