from fastapi import Depends

from api import app, session, schemas
from api.auth import token_auth

from . import application_entity, pipeline, container, user, dicom, destination

app.include_router(user.router, tags=['User'], prefix='/user')

# Secure Routes
app.include_router(application_entity.router, tags=['Application Entity'], prefix='/ae', dependencies=[Depends(token_auth)])
app.include_router(pipeline.router, tags=['Pipeline'], prefix='/pipeline', dependencies=[Depends(token_auth)])
app.include_router(container.router, tags=['Container'], prefix='/container', dependencies=[Depends(token_auth)])
app.include_router(dicom.router, tags=['Dicom'], prefix='/dicom', dependencies=[Depends(token_auth)])
app.include_router(destination.router, tags=['Destination'], prefix='/destination', dependencies=[Depends(token_auth)])
