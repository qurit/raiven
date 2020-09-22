from api import socketio, config, app as application

if __name__ == '__main__' and not config.IS_WORKER:
    opts = {'host': config.HOST, 'port': config.PORT, 'debug': True}

    # if config.WEB_SOCKETS_ENABLED:
    #     socketio.run(application, use_reloader=False, **opts)
    # else:
    application.run(**opts)
