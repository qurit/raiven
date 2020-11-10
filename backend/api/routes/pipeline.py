from api.schemas import pipeline as schemas
from api.controllers.pipeline import PipelineController
from api.models.pipeline import Pipeline, PipelineLink, PipelineNode, PipelineRun
from api import session
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import StreamingResponse

import os
import zipfile
import io


router = APIRouter()


@router.get("/runs")
def get_all_pipeline_runs(db: Session = Depends(session)):
    return db.query(PipelineRun).all()


@router.get("/download/{pipeline_run_id}")
def download_pipeline_run(pipeline_run_id: int, db: Session = Depends(session)):

    pipeline_run = db.query(
        PipelineRun).get(pipeline_run_id)

    result_path = os.path.join(
        pipeline_run.get_abs_path(), "output")

    result_files = (os.listdir(os.path.join(
        pipeline_run.get_abs_path(), "output")))

    # downloading all the files in the output into a zip file
    compression = zipfile.ZIP_DEFLATED
    zf = zipfile.ZipFile("results.zip", mode="w")
    for file_name in result_files:
        zf.write(os.path.join(result_path, file_name),
                 file_name, compress_type=compression)
    zf.close()

    # sending the zip file as response
    zip_file = open("results.zip", 'rb')
    response = StreamingResponse(
        zip_file, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = "attachment; filename=results.zip"
    return response


@ router.get("/", response_model=List[schemas.Pipeline])
def get_all_pipelines(db: Session = Depends(session)):
    return db.query(Pipeline).all()


@ router.post("/", response_model=schemas.Pipeline)
def create_pipeline(pipeline: schemas.PipelineCreate, db: Session = Depends(session)):
    print("got here")
    print(pipeline)
    return Pipeline(**pipeline.dict()).save(db)


@ router.get("/{pipeline_id}", response_model=schemas.PipelineFull)
def get_pipeline(pipeline_id: int, db: Session = Depends(session)):
    return db.query(Pipeline).get(pipeline_id)


@ router.put("/{pipeline_id}", response_model=schemas.PipelineRun)
def run_pipeline(pipeline_id: int, run_options: schemas.PipelineRunOptions, background_tasks: BackgroundTasks, db: Session = Depends(session)):
    """ Runs A Pipeline. """
    run_options.pipeline_id = pipeline_id
    run = PipelineController(db).create_pipeline_run(run_options)
    db.commit()

    background_tasks.add_task(PipelineController.run_pipeline_task, run.id)

    return run


# TODO: ask Adam why this didnt send the x and y coordinates... even tho they're defined in the model?
# @router.get("/{pipeline_id}/nodes", response_model=List[schemas.PipelineNode])
@ router.get("/{pipeline_id}/nodes")
def get_pipeline_nodes(pipeline_id: int, db: Session = Depends(session)):
    return db.query(PipelineNode).filter(PipelineNode.pipeline_id == pipeline_id).all()


@ router.get("/{pipeline_id}/links")
def get_pipeline_links(pipeline_id: int, db: Session = Depends(session)):
    return db.query(PipelineLink).filter(PipelineLink.pipeline_id == pipeline_id).delete()


@ router.post("/{pipeline_id}", response_model=schemas.Pipeline)
def update_pipeline(pipeline_id: int, pipeline_update: schemas.PipelineUpdate, db: Session = Depends(session)):
    """ This Allows you to update / add pipeline containers and links """
    print("pipeline payload from frontend")
    print(pipeline_update)

    # clear out any previous nodes / links
    db.query(PipelineNode).filter(
        PipelineNode.pipeline_id == pipeline_id).delete()
    db.query(PipelineLink).filter(
        PipelineLink.pipeline_id == pipeline_id).delete()
    # save new nodes and links
    nodes = {node.node_id: PipelineNode(
        pipeline_id=pipeline_id,
        container_id=node.container_id,
        x_coord=node.x,
        y_coord=node.y,
        container_is_input=node.container_is_input,
        container_is_output=node.container_is_output
    ).save(db) for node in pipeline_update.nodes}

    for link in pipeline_update.links:
        PipelineLink(
            pipeline_id=pipeline_id,
            to_node_id=nodes[link.to].id,
            from_node_id=nodes[link.from_].id
        ).save(db)

    return db.query(Pipeline).get(pipeline_id)


@ router.delete("/{pipeline_id}", response_model=schemas.Pipeline)
def delete_pipeline(pipeline_id: int, db: Session = Depends(session)):
    return db.query(Pipeline).get(pipeline_id).delete(db)
