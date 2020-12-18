import os
import pathlib

from api.routes.container import create_container, delete_container
from api.models.container import Container

from tests import testing_session, utils


# noinspection DuplicatedCode
def test_container_create_zip(db):
    assert os.path.exists(mock_path := os.path.join(os.path.dirname(__file__), 'mock_data'))
    assert os.path.exists(file_path := os.path.join(mock_path, 'simple_container.zip'))
    assert os.path.isfile(file_path)

    with open(file_path, 'rb') as fp:
        data = fp.read()

    container: Container = create_container(
        auto_build=False,
        file=data,
        name='test_container_create_zip',
        filename='simple_container.zip',
        description='A simple container',
        is_input_container=False,
        is_output_container=False,
        is_shared=False,
        user=utils.get_test_user(db),
        db=db
    )

    assert type(container) is not list
    assert type(container) is Container
    assert pathlib.Path(abs_path := container.get_abs_path()).exists()
    assert not pathlib.Path(container.get_path()).is_absolute()
    assert container.dockerfile_path == pathlib.Path(container.dockerfile_path).as_posix()

    delete_container(container.id, db)
    assert not pathlib.Path(abs_path).exists()


