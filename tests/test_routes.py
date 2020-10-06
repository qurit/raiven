import os
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from api import app, schemas


client = TestClient(app)


def test_get_pipelines() -> dict:
    response = client.get('/pipeline/')
    assert response.status_code == 200

    return response.json()


def test_add_pipeline(pipeline_create: schemas.pipeline.PipelineCreate = None) -> dict:
    if not pipeline_create:
        pipeline_create = schemas.pipeline.PipelineCreate(name='Test Pipeline')

    response = client.post("/pipeline/", json=pipeline_create.dict())

    assert response.status_code == 200
    assert response.json()['name'] == pipeline_create.name

    return response.json()


def test_update_pipeline():
    pass


def test_delete_pipeline(pipeline_id: int = None):
    if not pipeline_id:
        p = schemas.pipeline.PipelineCreate(name='Test Add')
        pipeline_id = test_add_pipeline(p)['id']

    response = client.delete(f'/pipeline/{pipeline_id}')
    assert response.status_code == 200
