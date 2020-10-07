import os
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form

from api import session, config
from api.schemas import container
from api.models.container import Container

router = APIRouter()


@router.get("/", response_model=List[container.Container])
def get_all_containers(db: Session = Depends(session)):
    """ Get a list of containers """

    return db.query(Container).all()


@router.post("/")
async def create_container(file: bytes = File(...), name: str = Form(...), filename: str = Form(...), description: str = Form(...), is_input_container: bool = Form(...), is_output_container: bool = Form(...),  db: session = Depends(session)):
    # TODO: maybe change to user_id directory or something?
    save_path = 'user_files'
    # write file to local storage. added the underscore so users can add mutliple dockerfiles to same directory
    complete_path = os.path.join(save_path, filename + '_' + name)
    file_ = open(complete_path, "wb")
    file_.write(file)
    file_.close()

    # save container to databse
    new_container = container.ContainerCreate(user_id=1, name=filename, description=description,
                                              dockerfile_path=complete_path, is_input_container=is_input_container, is_output_container=is_output_container)
    db_container = Container(**new_container.dict())
    db_container.save(db)

    return db_container


@router.get("/{container_id}", response_model=container.Container)
def get_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id)


@router.delete("/{container_id}", response_model=container.Container)
def delete_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id).delete(db)
