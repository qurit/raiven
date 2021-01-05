import os

import pytest

from api.routes.container import create_container, delete_container
from tests import utils, testing_session


@pytest.fixture(scope="module")
def example_container():
    assert os.path.exists(mock_path := os.path.join(os.path.dirname(__file__), 'mock_data'))
    assert os.path.exists(file_path := os.path.join(mock_path, 'simple_container.zip'))
    assert os.path.isfile(file_path)

    with open(file_path, 'rb') as fp:
        data = fp.read()

    with testing_session() as db:
        container = create_container(
            auto_build=False,
            file=data,
            name='Test Container',
            filename='simple_container.zip',
            description='A simple container',
            is_input_container=False,
            is_output_container=False,
            is_shared=False,
            user=utils.get_test_user(db),
            db=db
        )

        yield container

        delete_container(container_id=container.id, db=db)


@pytest.fixture()
def malformed_container():
    with testing_session() as db:
        container = create_container(
            auto_build=False,
            file=b'Pythons are cool',
            name='Test Container',
            filename='Dockerfile',
            description='A simple container',
            is_input_container=False,
            is_output_container=False,
            is_shared=False,
            user=utils.get_test_user(db),
            db=db
        )

        yield container

        delete_container(container_id=container.id, db=db)

