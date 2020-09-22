from fastapi import Depends

from api import app, session, schemas

from . import application_entity


app.include_router(application_entity.router, tags=['Application Entity'], prefix='/ae')
