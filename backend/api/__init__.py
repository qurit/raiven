import passlib
from config import BaseConfig
config = BaseConfig()


from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .database import session, worker_session, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# TODO: delete postman origin
# adding postman here for testing purposes for now 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://web.postman.co"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from . import routes


from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get('/')
def secure_route(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# Start the Dicom Server
from .dicom import SCP
scp_server = SCP(ae_title=config.SCP_AE_TITLE, host=config.SCP_HOST, port=config.SCP_PORT)
scp_server.start_server(blocking=False)
