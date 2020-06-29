from tests import docker


def test_connection():
    assert docker.containers.list(), "Can't connect to docker daemon"
