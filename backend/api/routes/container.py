import os
import zipfile
import io
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

    newContainerList = []

    # need to check why zipfile.is_zip(file) didn't work
    if ".zip" in filename:
        z = zipfile.ZipFile(io.BytesIO(file))
        for file in z.namelist():
            db_container1 = Container(
                user_id=1,
                name=name,
                description=description,
                is_input_container=is_input_container,
                is_output_container=is_output_container,
                filename=file)
            db_container1.save(db)
            db_container1.dockerfile_path = os.path.join(
                db_container1.path, file)
            db_container1.save(db)
            z.extract(file, path=os.path.join(
                db_container1.abs_path))
            newContainerList.append(db_container1)
    else:
        db_container = Container(
            user_id=1,
            name=name,
            description=description,
            is_input_container=is_input_container,
            is_output_container=is_output_container,
            filename=filename)
        db_container.save(db)
        with open(os.path.join(db_container.abs_path, filename), 'wb') as fp:
            fp.write(file)
        db_container.dockerfile_path = os.path.join(
            db_container.path, filename)
        db_container.save(db)
        newContainerList.append(db_container)
    return newContainerList


@ router.get("/{container_id}", response_model=container.Container)
def get_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id)


@ router.put("/{container_id}")
def update_container(container_id: int, file: bytes = File(None), name: str = Form(...), filename: str = Form(None), description: str = Form(None), is_input_container: bool = Form(...), is_output_container: bool = Form(...),  db: session = Depends(session)):
    if (file != None):
        container = db.query(Container).get(container_id)
        # remove previous file
        os.remove(os.path.join(container.abs_path, container.filename))
        # write new file
        with open(os.path.join(container.abs_path, filename), 'wb') as fp:
            fp.write(file)
        db.query(Container).filter(Container.id == container_id).update({
            "name": name,
            "description": description,
            "is_input_container": is_input_container,
            "is_output_container": is_output_container,
            "dockerfile_path": os.path.join(container.path, filename),
            "filename": filename
        })
        return db.query(Container).get(container_id)
    else:
        db.query(Container).filter(Container.id == container_id).update({
            "name": name,
            "description": description,
            "is_input_container": is_input_container,
            "is_output_container": is_output_container
        })
        return db.query(Container).get(container_id)


@ router.delete("/{container_id}", response_model=container.Container)
def delete_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id).delete(db)
