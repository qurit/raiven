import pathlib

from api.routes.container import create_container, delete_container
from api.models.container import Container

from tests import testing_session, utils


def test_container_create_zip():

    with open('C:\\Users\\Adam\\Programming\\picom\\examples\\simple_container.zip', 'rb') as fp:
        data = fp.read()

    with testing_session() as db:
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
        )[0]

        assert type(container) is Container
        assert pathlib.Path(abs_path := container.get_abs_path()).exists()
        assert not pathlib.Path(container.get_path()).is_absolute()
        assert container.get_path() == pathlib.Path(container.get_path()).as_posix()

        delete_container(container.id, db)
        assert not pathlib.Path(abs_path).exists()


if __name__ == '__main__':
    test_container_create_zip()

