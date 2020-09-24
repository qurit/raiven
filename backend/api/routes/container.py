from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from api import session, schemas
from api.models.pipeline import Container

router = APIRouter()


@router.get("/", response_model=List[schemas.Container])
def get_all_containers(db: Session = Depends(session)):
    return db.query(Container).all()


@router.post("/", response_model=schemas.Container)
def create_container(container: schemas.ContainerCreate, db: Session = Depends(session)):
    return Container(**container.dict()).save(db)


@router.get("/{container_id}", response_model=schemas.Container)
def get_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id)


@router.delete("/{container_id}", response_model=schemas.Pipeline)
def delete_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id).delete(db)
