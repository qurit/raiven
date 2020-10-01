import os
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form

from api import session, schemas, config
from api.models.pipeline import Container

router = APIRouter()


@router.get("/", response_model=List[schemas.Container])
def get_all_containers(db: Session = Depends(session)):
    """ Get a list of containers """

    return db.query(Container).all()


@router.post("/", response_model=schemas.Container)
def create_container(container: schemas.ContainerCreate, db: Session = Depends(session)):
    """ Allows the creation of a new container """
    return Container(**container.dict()).save(db)


@router.post("/{container_id}", response_model=schemas.Container)
def upload_dockerfile(container_id: int, dockerfile: bytes = File(...), db: Session = Depends(session)):
    """ Allows the upload of dockerfile to be used with a container """
    container = db.query(Container).get(container_id)
    dockerfile_path = os.path.join(container.get_path(), 'dockerfile')

    with open(dockerfile_path) as fp:
        fp.write(dockerfile)

    return container


@router.get("/{container_id}", response_model=schemas.Container)
def get_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id)


@router.delete("/{container_id}", response_model=schemas.Container)
def delete_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id).delete(db)
