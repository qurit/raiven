import pathlib
import io
import os
import zipfile
from typing import List

from fastapi import APIRouter, Depends, File, Form
from sqlalchemy.orm import Session

from api import session, config
from api.models.container import Container, Tag, ContainerTags
from api.schemas import container
from api.pipelining import ContainerController
from api.models.user import User
from api.auth import token_auth

router = APIRouter()


@router.get("/stats", response_model=container.ContainerStats)
def get_container_stats(db: Session = Depends(session)):
    """ Get container count. Used in dashboard counter."""
    stats = {
        "container_counts": db.query(Container).count(),
    }
    return stats


@router.get("/", response_model=List[container.Container])
def get_all_containers(user: User = Depends(token_auth), db: Session = Depends(session)):
    """ Get a list of containers. Returns a list of all containers created by the user OR shared with the user"""

    return db.query(Container).filter((Container.user_id == user.id) | Container.is_shared).all()


@router.get("/tags", response_model=List[container.Tag])
def get_tags(db: Session = Depends(session)):
    return db.query(Tag).all()


@router.post("/tags", response_model=List[container.Tag])
def post_tags(tags: List[str], db: Session = Depends(session)):
    new_tags = []
    for tag in tags:
        exists = db.query(Tag.id).filter_by(tag_name=tag).first() is not None
        if not exists:
            new_tag = Tag(tag_name=tag)
            new_tag.save(db)
            new_tags.append(new_tag)
    return new_tags


@router.post("/{container_id}/tags", response_model=List[str])
def post_container_tags(container_id: int, tags: List[str], db: Session = Depends(session)):
    db.query(ContainerTags).filter(ContainerTags.container_id == container_id).delete()
    for tag in tags:
        tag = db.query(Tag).filter_by(tag_name=tag).first()
        tag_id = tag.id
        new_container_tag = ContainerTags(container_id=container_id, tag_id=tag_id)
        new_container_tag.save(db)
    return tags


@router.post("/", response_model=container.Container)
def create_container(auto_build: bool = True,
                     file: bytes = File(...), name: str = Form(...), filename: str = Form(...),
                     description: str = Form(None), is_input_container: bool = Form(...),
                     is_output_container: bool = Form(...), is_shared: bool = Form(...), user: User = Depends(token_auth), db: Session = Depends(session)):

    db_container = Container(
        user_id=user.id,
        name=name,
        description=description,
        is_input_container=is_input_container,
        is_output_container=is_output_container,
        is_shared=is_shared,
        filename='Dockerfile')
    db_container.save(db)

    # TODO: fix this zip file check, tried zipfile.is_zipfile() but didn't work
    if ".zip" in filename:
        z = zipfile.ZipFile(io.BytesIO(file))
        folder = db_container.get_abs_path()
        z.extractall(folder)

        # Finding the Dockerfile in the zip file
        for root, _, files in os.walk(folder):
            if 'Dockerfile' in files:
                dockerfile_path = os.path.relpath(root, config.UPLOAD_DIR)
                db_container.dockerfile_path = (pathlib.Path(dockerfile_path) / 'Dockerfile').as_posix()
                break

        db_container.save(db)

    else:
        with open(os.path.join(db_container.get_abs_path(), filename), 'wb') as fp:
            fp.write(file)

        db_container.save(db)

    # Build Container In Background
    db.commit()

    # if auto_build:
    #     ContainerController.build_container(db_container.id)

    print(db_container)
    return db_container


@router.get("/{container_id}", response_model=container.Container)
def get_container(container_id: int, db: Session = Depends(session)):
    """ Get a specific container"""
    container_schema = container.Container.from_orm(
        db.query(Container).get(container_id)
    )

    tags: List[str] = db.query(Tag.tag_name).join(ContainerTags).filter_by(container_id=container_id).all()
    container_schema.tags = [t[0] for t in tags]

    return container_schema


@router.put("/{container_id}", response_model=container.Container)
def update_container(
        container_id: int, file: bytes = File(None), name: str = Form(...), filename: str = Form(None),
        description: str = Form(None), is_input_container: bool = Form(...), is_output_container: bool = Form(...), is_shared: bool = Form(...),
        db: session = Depends(session)):
    """ Editing a container"""
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
            "is_shared": is_shared,
            "dockerfile_path": os.path.join(container.get_path(), filename),
            "filename": filename
        })
        return db.query(Container).get(container_id)
    else:
        db.query(Container).filter(Container.id == container_id).update({
            "name": name,
            "description": description,
            "is_input_container": is_input_container,
            "is_output_container": is_output_container,
            "is_shared": is_shared
        })
        return db.query(Container).get(container_id)


@router.delete("/{container_id}", response_model=container.Container)
def delete_container(container_id: int, db: Session = Depends(session)):
    """ Delete a container"""
    return db.query(Container).get(container_id).delete(db)
