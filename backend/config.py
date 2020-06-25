class BaseConfig(object):

    SECRET_KEY = 'replace_me!'

    # DB SETTINGS
    MONGO_USER = 'picom_admin'
    MONGO_PASSWORD = 'password'
    MONGO_HOST = 'mongo'
    MONGO_PORT = 27017
    MONGO_DB = 'picom'
    MONGO_URI = "mongodb://{}:{}@{}:{}/{}".format(MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DB)
