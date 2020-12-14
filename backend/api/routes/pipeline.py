import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api import session, queries, middleware
from api.pipelining import PipelineController
from api.models.pipeline import Pipeline, PipelineLink, PipelineNode, PipelineRun
from api.schemas import pipeline as schemas
from api.models.user import User
from api.auth import token_auth

router = APIRouter()


@router.get("/stats")
def get_pipeline_stats(db: Session = Depends(session)):
    stats = {
        "pipeline_counts": db.query(Pipeline).count(),
        "pipeline_run_counts": db.query(PipelineRun).count()
    }
    return stats


@router.get("/runs")
def get_all_pipeline_runs(limit: int = 7, db: Session = Depends(session)):
    return queries.group_by_date(db, PipelineRun.created_datetime, limit=limit)


@router.get("/results", response_model=List[schemas.PipelineRun])
def get_all_pipeline_runs(user: User = Depends(token_auth), db: Session = Depends(session)):
    return db.query(PipelineRun).join(Pipeline).filter(Pipeline.user_id == user.id).all()


@router.get("/download/{pipeline_run_id}")
def download_pipeline_run(pipeline_run_id: int, db: Session = Depends(session)):
    pipeline_run: PipelineRun = db.query(PipelineRun).get(pipeline_run_id)
    result_path = pipeline_run.get_abs_output_path()
    zip_path = os.path.join(pipeline_run.get_abs_path(), 'result')

    # Creating a zip file if it doesn't exist'
    if not os.path.exists(zip_path):
        shutil.make_archive(zip_path, 'zip', result_path)

    # Sending the zip file as response
    zip_file = open(zip_path + '.zip', 'rb')
    response = StreamingResponse(zip_file, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = "attachment; filename=results.zip"

    return response


@ router.get("/", response_model=List[schemas.Pipeline])
def get_all_pipelines(user: User = Depends(token_auth), db: Session = Depends(session)):
    return db.query(Pipeline).filter((Pipeline.user_id == user.id) | Pipeline.is_shared).all()


@router.post("/", response_model=schemas.Pipeline)
def create_pipeline(pipeline: schemas.PipelineCreate, user: User = Depends(token_auth), db: Session = Depends(session)):
    return(Pipeline(name=pipeline.name, ae_title=pipeline.ae_title, is_shared=pipeline.is_shared, user_id=user.id)).save(db)


@router.get("/{pipeline_id}", response_model=schemas.PipelineFull)
def get_pipeline(pipeline_id: int, db: Session = Depends(session)):
    if not (pipeline := db.query(Pipeline).get(pipeline_id)):
        raise HTTPException(404)

    return pipeline


@router.put("/{pipeline_id}", response_model=schemas.PipelineRun)
def run_pipeline(pipeline_id: int, run_options: schemas.PipelineRunOptions, db: Session = Depends(session)):
    """ Runs A Pipeline. """
    run = PipelineController.pipeline_run_factory(
        db, run_options.get_cls_type(), run_options.dicom_obj_id, pipeline_id)
    db.commit()

    PipelineController.run_pipeline_task(db, run)
    return run


@ router.get("/{pipeline_id}/nodes", response_model=List[schemas.PipelineNode])
def get_pipeline_nodes(pipeline_id: int, db: Session = Depends(session)):
    return db.query(PipelineNode).filter(PipelineNode.pipeline_id == pipeline_id).all()


@router.get("/{pipeline_id}/links")
def get_pipeline_links(pipeline_id: int, db: Session = Depends(session)):
    return db.query(PipelineLink).filter(PipelineLink.pipeline_id == pipeline_id).delete()


@router.post("/{pipeline_id}", response_model=schemas.Pipeline)
def update_pipeline(pipeline_id: int, pipeline_update: schemas.PipelineUpdate, db: Session = Depends(session)):
    """ This Allows you to update / add pipeline containers and links """

    # clear out any previous nodes / links
    db.query(PipelineNode).filter(PipelineNode.pipeline_id == pipeline_id).delete()
    db.query(PipelineLink).filter(PipelineLink.pipeline_id == pipeline_id).delete()

    # save new nodes and links
    nodes = {node.node_id: PipelineNode(
        pipeline_id=pipeline_id,
        container_id=node.container_id,
        x_coord=node.x,
        y_coord=node.y,
        container_is_input=node.container_is_input,
        container_is_output=node.container_is_output,
        destination_id=node.destination_id
    ).save(db) for node in pipeline_update.nodes}

    for link in pipeline_update.links:
        PipelineLink(
            pipeline_id=pipeline_id,
            to_node_id=nodes[link.to].id,
            from_node_id=nodes[link.from_].id
        ).save(db)

    return db.query(Pipeline).get(pipeline_id)


@router.delete("/{pipeline_id}", response_model=schemas.Pipeline)
@middleware.exists_or_404
def delete_pipeline(pipeline_id: int, db: Session = Depends(session)):
    if pipeline := db.query(Pipeline).get(pipeline_id):
        pipeline.delete(db)

    return pipeline
