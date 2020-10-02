from fastapi import Depends

from api import app, session, schemas

from . import application_entity, pipeline, container, user


app.include_router(application_entity.router, tags=[
                   'Application Entity'], prefix='/ae')
app.include_router(pipeline.router, tags=['Pipeline'], prefix='/pipeline')
app.include_router(container.router, tags=['Container'], prefix='/container')


# TODO: delete later, just need it for now for the container add thing
app.include_router(user.router, tags=['User'], prefix='/user')
