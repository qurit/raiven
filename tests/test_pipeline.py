import os
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from api import app, schemas
from tests.test_container import test_add_container

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
    container_1 = test_add_container()
    container_2 = test_add_container()
    pipeline = test_add_pipeline()

    nodes = [
        schemas.pipeline.PipelineNodeCreate(container_id=container_1['id'], x=0, y=1).dict(),
        schemas.pipeline.PipelineNodeCreate(container_id=container_2['id'], x=50, y=-10).dict()
    ]
    links = [{'to': 0, 'from': 1}]
    pipeline_update = {
        'nodes': nodes,
        'links': links
    }

    response = client.post(f"/pipeline/{pipeline['id']}", json=pipeline_update)
    assert response.status_code == 200, response.json()


def test_delete_pipeline(pipeline_id: int = None):
    if not pipeline_id:
        p = schemas.pipeline.PipelineCreate(name='Test Add')
        pipeline_id = test_add_pipeline(p)['id']

    response = client.delete(f'/pipeline/{pipeline_id}')
    assert response.status_code == 200
