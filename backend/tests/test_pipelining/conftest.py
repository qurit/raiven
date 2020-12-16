import pytest
from dramatiq import Worker

# noinspection PyProtectedMember
from api.pipelining._tasks import broker
from api.routes.container import create_container, delete_container


from tests import utils, testing_session


@pytest.fixture()
def stub_broker():
    broker.flush_all()
    return broker


@pytest.fixture()
def stub_worker():
    worker = Worker(broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()


@pytest.fixture(scope="module")
def example_container():

    with open('C:\\Users\\Adam\\Programming\\picom\\examples\\simple_container.zip', 'rb') as fp:
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

