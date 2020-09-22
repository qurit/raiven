import uvicorn

from api import config, app as application

if __name__ == '__main__':
    uvicorn.run('asgi:application', host=config.HOST, port=config.PORT, reload=True)
