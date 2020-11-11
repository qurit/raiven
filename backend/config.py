import os
from distutils.util import strtobool

LOCALHOST = '127.0.0.1'


class BaseConfig:
    RAIVEN_WORKER = False

    APT_HOST = '127.0.0.1'
    API_PORT = 5000
    API_HOT_RELOAD = True
    UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

    # Auth
    SECRET_KEY = 'ChangeMe'
    TOKEN_TTL = 3600

    # LDAP CONFIG
    LDAP_HOST = '10.9.2.37'
    LDAP_PORT = 389
    LDAP_USE_SSL = False
    LDAP_USERNAME_BASE = 'CRC\\'
    LDAP_BASE_DN = 'DC=BCCRC,DC=CA'
    LDAP_TEST_USR = 'crcldapviewer'
    LDAP_TEST_PW = 'LD@P2020pw!'

    # DB Config
    POSTGRES_HOST = '127.0.0.1'
    POSTGRES_USER = 'postgres'
    POSTGRES_PW = 'password'
    POSTGRES_DB = 'raiven'
    SQLALCHEMY_DATABASE_URI = ''

    # Docker
    DOCKER_URI = 'tcp://127.0.0.1:2375'

    # RabbitMQ
    RABBITMQ_HOST = '127.0.0.1'

    # Pipeline
    PICOM_INPUT_DIR = '/mnt/picom/input'
    PICOM_OUTPUT_DIR = '/mnt/picom/output'
    IMAGE_TAG_PREFIX = 'RAIVEN'

    # DICOM
    SCP_AE_TITLE = 'RAIVEN'
    SCP_HOST = '127.0.0.1'
    SCP_PORT = 11112

    def __init__(self):
        env_vars = [v for v in os.environ.keys() if (v in vars(BaseConfig)) and not v.startswith('__')]
        [self.apply_env_var(k) for k in env_vars]

        if not os.path.exists(self.UPLOAD_DIR):
            os.mkdir(self.UPLOAD_DIR)

        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PW}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}'

        # if not hasattr(self, 'RABBITMQ_URI'):
        #     self.RABBITMQ_URI = f'amqp://{self.RABBITMQ_HOST}'

    def apply_env_var(self, env_var) -> None:
        v = os.environ[env_var]

        try:
            type_ = type(getattr(BaseConfig, env_var))
            if type_ is bool:
                v = strtobool(v)
            else:
                v = type_(v)
        except (TypeError, ValueError):
            print(
                f'[FAILED] TYPE CASTING ENV VARIABLE {env_var} TO TYPE {type(getattr(BaseConfig, env_var))}')
            print(
                f'[FAILED] ENV VARIABLE {env_var} MAY PRODUCE AN UNEXPECTED ERROR')
        finally:
            print('[config]', env_var, v)
            setattr(self, env_var, v)
