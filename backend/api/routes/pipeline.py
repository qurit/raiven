from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from api import session
from api.models.pipeline import Pipeline, PipelineLink, PipelineNode
from api.schemas import pipeline as schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Pipeline])
def get_all_pipelines(db: Session = Depends(session)):
    return db.query(Pipeline).all()


@router.post("/", response_model=schemas.Pipeline)
def create_pipeline(pipeline: schemas.PipelineCreate, db: Session = Depends(session)):
    print("got here")
    print(pipeline)
    return Pipeline(**pipeline.dict()).save(db)


@router.get("/{pipeline_id}", response_model=schemas.PipelineFull)
def get_pipeline(pipeline_id: int, db: Session = Depends(session)):
    return db.query(Pipeline).get(pipeline_id)


@router.post("/{pipeline_id}", response_model=schemas.Pipeline)
def update_pipeline(pipeline_id: int, pipeline_update: schemas.PipelineUpdate, db: Session = Depends(session)):
    """ This Allows you to update / add pipeline containers and links """

    nodes = [PipelineNode(
        pipeline_id=pipeline_id,
        container_id=node.container_id,
        x_coord=node.x,
        y_coord=node.y
    ).save(db) for node in pipeline_update.nodes]
    print(pipeline_update)

    for link in pipeline_update.links:
        pipeline_link = PipelineLink(pipeline_id=pipeline_id)

        try:
            if link.to:
                pipeline_link.to_node_id = nodes[link.to].id

            if link.from_:
                pipeline_link.from_node_id = nodes[link.from_].id
        except KeyError:
            print("Invalid Link")
        else:
            pipeline_link.save(db)

    return db.query(Pipeline).get(pipeline_id)


@router.delete("/{pipeline_id}", response_model=schemas.Pipeline)
def delete_pipeline(pipeline_id: int, db: Session = Depends(session)):
    return db.query(Pipeline).get(pipeline_id).delete(db)