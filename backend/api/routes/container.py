import io
import os
import zipfile
from typing import List

from fastapi import APIRouter, Depends, File, Form
from sqlalchemy.orm import Session

from api import session, config
from api.models.container import Container
from api.schemas import container
from api.pipelining import ContainerController

router = APIRouter()


@router.get("/stats")
def get_container_stats(db: Session = Depends(session)):
    stats = {
        "container_counts": db.query(Container).count(),
    }
    return stats


@router.get("/", response_model=List[container.Container])
def get_all_containers(db: Session = Depends(session)):
    """ Get a list of containers """

    return db.query(Container).all()


# TODO: Add response model
@router.post("/")
async def create_container(
        file: bytes = File(...), name: str = Form(...), filename: str = Form(...),
        description: str = Form(None), is_input_container: bool = Form(...),
        is_output_container: bool = Form(...), db: session = Depends(session)):

    if ".zip" in filename:
        z = zipfile.ZipFile(io.BytesIO(file))
        db_container = Container(
            user_id=1,  # TODO: Add user
            name=name,
            description=description,
            is_input_container=is_input_container,
            is_output_container=is_output_container,
            filename='Dockerfile')
        db_container.save(db)

        folder = db_container.get_abs_path()
        z.extractall(folder)
        print(folder)
        for root, _, files in os.walk(folder):
            print(root, _, files)
            if 'Dockerfile' in files:
                db_container.dockerfile_path = os.path.relpath(os.path.join(root, 'Dockerfile'), config.UPLOAD_DIR)
                break

        db_container.save(db)
    else:
        # TODO: Review This Code.  Refactoring needed
        db_container = Container(
            user_id=1,
            name=name,
            description=description,
            is_input_container=is_input_container,
            is_output_container=is_output_container,
            filename=filename)
        db_container.save(db)
        with open(os.path.join(db_container.get_abs_path(), filename), 'wb') as fp:
            fp.write(file)
        db_container.dockerfile_path = os.path.join(db_container.get_path(), filename)
        db_container.save(db)

    # Build Container In Background
    db.commit()
    ContainerController.build_container(db_container.id)

    # TODO: We shoulnt return a list
    return [db_container]


@router.get("/{container_id}", response_model=container.Container)
def get_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id)


@router.put("/{container_id}")
def update_container(
        container_id: int, file: bytes = File(None), name: str = Form(...), filename: str = Form(None),
        description: str = Form(None), is_input_container: bool = Form(...), is_output_container: bool = Form(...),
        db: session = Depends(session)):

    if file is not None:
        container = db.query(Container).get(container_id)
        # remove previous file
        os.remove(os.path.join(container.get_abs_path(), container.filename))
        # write new file
        with open(os.path.join(container.get_abs_path(), filename), 'wb') as fp:
            fp.write(file)
        db.query(Container).filter(Container.id == container_id).update({
            "name": name,
            "description": description,
            "is_input_container": is_input_container,
            "is_output_container": is_output_container,
            "dockerfile_path": os.path.join(container.get_path(), filename),
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


@router.delete("/{container_id}", response_model=container.Container)
def delete_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id).delete(db)
