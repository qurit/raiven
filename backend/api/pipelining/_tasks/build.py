from api import worker_session, models
from . import docker, utils, dramatiq


@dramatiq.actor
def build_container_task(container_id: int):
    print(f"BUILDING CONTAINER: {container_id}")

    with worker_session() as db:
        container = models.container.Container.query(db).get(container_id)
        container_build = models.container.ContainerBuild(
            container_id=container.id,
            status='building'
        )
        build_path = container.build_abs_path
        container_build.save(db)
        tag = utils.validate_tag(container_build.generate_tag())

    image, build_logs = docker.images.build(path=build_path, tag=tag)
    with worker_session() as db:
        container_build.status = 'exited'
        container_build.exit_code = 0
        container_build.tag = image.tags[0]
        container_build.save(db)
