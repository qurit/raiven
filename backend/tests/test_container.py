import io

from api.schemas.container import ContainerCreate

from . import client
from .utils import get_test_user


def test_add_container(form_data: dict = None, user_id: int = None, file: bytes = None) -> dict:
    if not form_data:
        form_data = {
            "user_id": None,
            "name": 'Default Container',
            "description": 'A Default Container',
            "filename": 'Dockerfile',
            "is_input_container": False,
            "is_output_container": False
            "filename": "Dockerfile Name"
        }

    form_data["user_id"] = user_id if user_id else get_test_user().id
    form_data['file'] = file if file else (
        io.BytesIO(b"test bytes"), 'test.jpg')
    response = client.post('/container/', data=form_data)

    print(response.json())
    assert response.status_code == 200
    return response.json()


def test_get_containers() -> dict:
    response = client.get('/container/')
    assert response.status_code == 200
    assert type(response.json()) is list
