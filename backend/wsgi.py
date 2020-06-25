from api import socketio, config, app as application

if __name__ == '__main__':
    opts = {'host': config.HOST, 'port': config.PORT, 'debug': True}

    if config.WEB_SOCKETS_ENABLED:
        socketio.run(application, **opts)
    else:
        application.run(**opts)
