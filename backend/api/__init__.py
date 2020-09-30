from config import BaseConfig
config = BaseConfig()


from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .database import session, engine
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
