# noinspection PyProtectedMember
from api.pipelining._tasks.build import build_container_task


def test_container_build_background(example_container):
    build_container_task(example_container.id)


def test_container_build_background(stub_broker, stub_worker, example_container):
    build_container_task.send(example_container.id)
    stub_broker.join(build_container_task.queue_name, fail_fast=True)
    stub_worker.join()
