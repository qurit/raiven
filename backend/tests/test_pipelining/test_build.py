from api.pipelining._tasks import docker
from api.pipelining._tasks.build import build_container_task
from api.models.container import ContainerBuild, ContainerBuildError


def test_container_build_foreground(example_container):
    build_container_task(example_container.id)

    assert example_container.build
    assert example_container.build.status == 'exited'
    assert example_container.build.exit_code == 0
    assert example_container.build.tag
    assert example_container.build.timestamp
    assert not example_container.build.error

    assert docker.images.get(example_container.build.tag)


def test_container_build_background(stub_broker, stub_worker, example_container):
    build_container_task.send(example_container.id)
    stub_broker.join(build_container_task.queue_name, fail_fast=True)
    stub_worker.join()

    assert example_container.build
    assert example_container.build.status == 'exited'
    assert example_container.build.exit_code == 0
    assert example_container.build.tag
    assert example_container.build.timestamp
    assert not example_container.build.error

    assert docker.images.get(example_container.build.tag)


def test_build_fail(malformed_container):
    build_container_task(malformed_container.id)

    assert malformed_container.build
    assert malformed_container.build.status == 'exited'
    assert malformed_container.build.exit_code != 0
    assert malformed_container.build.error
    assert malformed_container.build.error.stderr
