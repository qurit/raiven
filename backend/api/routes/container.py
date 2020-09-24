from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from api import session, models, schemas
router = APIRouter()


@router.get("/", response_model=List[schemas.Pipeline])
def get_all_pipelines(db: Session = Depends(session)):
    return db.query(models.pipeline.Pipeline).all()


@router.post("/", response_model=schemas.Pipeline)
def create_pipeline(pipeline: schemas.PipelineCreate, db: Session = Depends(session)):
    return models.pipeline.Pipeline(**pipeline.dict()).save(db)


@router.get("/{pipeline_id}", response_model=schemas.Pipeline)
def get_pipeline(pipeline_id: int, db: Session = Depends(session)):
    return db.query(models.pipeline.Pipeline).get(pipeline_id)


@router.delete("/{pipeline_id}", response_model=schemas.Pipeline)
def delete_pipeline(pipeline_id: int, db: Session = Depends(session)):
    return db.query(models.pipeline.Pipeline).get(pipeline_id).delete(db)


@router.post("/{pipeline_id}/steps", response_model=schemas.Pipeline)
def create_pipeline_step(step: schemas.PipelineStepCreate, db: Session = Depends(session)):
    return models.pipeline.PipelineStep(**step.dict()).save(db)