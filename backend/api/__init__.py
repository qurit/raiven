from config import BaseConfig
config = BaseConfig()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import session, worker_session, engine
from . import models, schemas, sockets

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title='Raiven API',
    docs_url='/'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/ws', sockets.sio_app)

from . import routes, pipelining
