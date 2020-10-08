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
async def create_container(file: bytes = File(...), name: str = Form(...), filename: str = Form(...), description: str = Form(None), is_input_container: bool = Form(...), is_output_container: bool = Form(...),  db: session = Depends(session)):
    # TODO: maybe change to user_id directory or something?
    # if not os.path.exists('user_files'):
    #       os.mkdir('user_files')
    # # write file to local storage. added the underscore so users can add mutliple dockerfiles to same directory
    # complete_path = os.path.join('user_files', filename + '_' + name)
    # file_ = open(complete_path, "wb")
    # file_.write(file)
    # file_.close()

    # save container to database
    db_container = Container(
        user_id=1,
        name=name,
        description=description,
        is_input_container=is_input_container,
        is_output_container=is_output_container
    )
    db_container.save(db)

    with open(os.path.join(db_container.abs_path, filename), 'wb') as fp:
        fp.write(file)

    return db_container


@router.get("/{container_id}", response_model=container.Container)
def get_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id)


@router.put("/{container_id}")
def update_container(container_id: int, file: bytes = File(None), name: str = Form(...), filename: str = Form(...), description: str = Form(None), is_input_container: bool = Form(...), is_output_container: bool = Form(...),  db: session = Depends(session)):
    print(file)
    # do the save to file thing if there is a "file" and update the Container.filepath to go to that path
    return db.query(Container).filter(Container.id == container_id).update({
        "name": name,
        # TODO: add filename?
        # "filename": filename,
        "description": description,
        "is_input_container": is_input_container,
        "is_output_container": is_output_container
    })


@router.delete("/{container_id}", response_model=container.Container)
def delete_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id).delete(db)
