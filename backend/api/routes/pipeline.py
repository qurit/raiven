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

# make a route to get the nodes and links where the pipeline id is {pipeline_id}


# TODO: ask Adam why this didnt send the x and y coordinates... even tho they're defined in the model?
# @router.get("/{pipeline_id}/nodes", response_model=List[schemas.PipelineNode])
@router.get("/{pipeline_id}/nodes")
def get_pipeline_nodes(pipeline_id: int, db: Session = Depends(session)):
    print("in pipeline node")
    return db.query(PipelineNode).filter(PipelineNode.pipeline_id == pipeline_id).all()

# need this because want to delete any existing links and nodes before creating/updating pipeline nodes and links for this pipeline


@router.delete("/{pipeline_id}/nodes")
def delete_pipeline_nodes(pipeline_id: int, db: Session = Depends(session)):
    print("in delete pipeline nodes")
    return db.query(PipelineNode).filter(PipelineNode.pipeline_id == pipeline_id).delete()


@router.get("/{pipeline_id}/links")
def get_pipeline_links(pipeline_id: int, db: Session = Depends(session)):
    print("in pipeline link")
    return db.query(PipelineLink).filter(PipelineLink.pipeline_id == pipeline_id).all()

# need this because want to delete any existing links and nodes before creating/updating pipeline nodes and links for this pipeline


@router.delete("/{pipeline_id}/links")
def delete_pipeline_links(pipeline_id: int, db: Session = Depends(session)):
    print("in delete pipeline links")
    return db.query(PipelineLink).filter(PipelineLink.pipeline_id == pipeline_id).delete()


@router.post("/{pipeline_id}", response_model=schemas.Pipeline)
def update_pipeline(pipeline_id: int, pipeline_update: schemas.PipelineUpdate, db: Session = Depends(session)):
    """ This Allows you to update / add pipeline containers and links """

    print("LINKS")
    print(pipeline_update.links)
    print("NODES")
    print(pipeline_update.nodes)
    nodes = [PipelineNode(
        pipeline_id=pipeline_id,
        container_id=node.container_id,
        x_coord=node.x,
        y_coord=node.y
    ).save(db) for node in pipeline_update.nodes]
    for link in pipeline_update.links:
        pipeline_link = PipelineLink(pipeline_id=pipeline_id)

        try:
            if link.to:
                pipeline_link.to_node_id = nodes[link.to - 1].id

            if link.from_:
                pipeline_link.from_node_id = nodes[link.from_ - 1].id
        except KeyError:
            print("Invalid Link")
        else:
            pipeline_link.save(db)

    return db.query(Pipeline).get(pipeline_id)


@router.delete("/{pipeline_id}", response_model=schemas.Pipeline)
def delete_pipeline(pipeline_id: int, db: Session = Depends(session)):
    print("in delete")
    return db.query(Pipeline).get(pipeline_id).delete(db)
