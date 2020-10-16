from fastapi import Depends

from api import app, session, schemas

from . import application_entity, pipeline, container, user, dicom, destination


app.include_router(application_entity.router, tags=[
                   'Application Entity'], prefix='/ae')
app.include_router(pipeline.router, tags=['Pipeline'], prefix='/pipeline')
app.include_router(container.router, tags=['Container'], prefix='/container')
app.include_router(user.router, tags=['User'], prefix='/user')
app.include_router(dicom.router, tags=['Dicom'], prefix='/dicom')
app.include_router(destination.router, tags=[
                   'Destination'], prefix='/destination')
