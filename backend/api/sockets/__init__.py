from flask_socketio import SocketIO

from api import config, app


def init_socketio():
    return SocketIO(async_mode=config.ASYNC_MODE, message_queue=config.RABBITMQ_URI) if config.IS_WORKER else SocketIO(app, cors_allowed_origins="*", message_queue=config.RABBITMQ_URI)