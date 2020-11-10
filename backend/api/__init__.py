import passlib
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


from . import routes

# Start the Dicom Server
from .dicom import SCP
scp_server = SCP(ae_title=config.SCP_AE_TITLE, host=config.SCP_HOST, port=config.SCP_PORT)
scp_server.start_server(blocking=False)
