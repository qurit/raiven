from api import app

from . import application_entity

app.include_router(application_entity.router)
