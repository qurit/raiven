from fastapi import Depends

from api import app, session, schemas

from . import application_entity, pipeline, container


app.include_router(application_entity.router, tags=['Application Entity'], prefix='/ae')
app.include_router(pipeline.router, tags=['Pipeline'], prefix='/pipeline')
app.include_router(container.router, tags=['Container'], prefix='/container')
