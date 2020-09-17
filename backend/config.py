import os
from distutils.util import strtobool

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

    POSTGRES_HOST = LOCALHOST
    POSTGRES_USER = 'postgres'
    POSTGRES_PW = 'password'
    POSTGRES_DB = 'picom'

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
    def SQLALCHEMY_DATABASE_URI(self):
        return f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PW}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}?gssencmode=disable'

    @property
    def RABBITMQ_URI(self):
        return f'amqp://{self.RABBITMQ_HOST}'


class DockerConfig(BaseConfig):
    HOST = '0.0.0.0'
    RABBITMQ_HOST = 'picom_rabbit'
    DOCKER_URI = 'unix://var/run/docker.sock'

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PW}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}'


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

        if env_var in vars(BaseConfig) and not env_var.startswith('__'):
            # print(f'SETTING ENV VARIABLE {env_var}={os.environ[env_var]}')

            # Trying to typecast the correct type
            v = os.environ[env_var]
            try:
                type_ = type(getattr(BaseConfig, env_var))
                if type_ is bool:
                    v = strtobool(v)
                else:
                    v = type_(v)
            except (TypeError, ValueError):
                print(f'[FAILED] TYPE CASTING ENV VARIABLE {env_var} TO TYPE {type(getattr(BaseConfig, env_var))}')
                print('[FAILED] ENV VARIABLE {env_var} MAY PRODUCE ERROR')

            setattr(config, env_var, v)

    return config()



