import os
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from api import app
from api.schemas.container import ContainerCreate

client = TestClient(app)


def test_add_container(container: ContainerCreate = None) -> dict:
    if not container:
        container = ContainerCreate(
            user_id=1,
            name="Test Container",
            description="Test description",
            dockerfile_path="Whoops this shoulnt be in create",
            is_input_container=False,
            is_output_container=False,
        )

    response = client.post('/container/', json=container.dict())
    assert response.status_code == 200

    print(type(response.json()))
    print(response.json())
    return response.json()


def test_get_containers() -> dict:
    response = client.get('/container')
    assert response.status_code == 200
    assert type(response.json()) is list

