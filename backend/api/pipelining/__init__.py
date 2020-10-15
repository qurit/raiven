import os
import shutil
import docker
from api import config, worker_session, models

client = docker.from_env()


def build_container(container_id: int):
    print(f"BUILDING CONTAINER: {container_id}")

    with worker_session() as db:
        container = models.container.Container.query(db).get(container_id)
        print(container)

    return None
    # client.build()


def run_node(run_id: int, node_id: int, previous_job_id: int = None):
    print(f"RUNNING NODE: {node_id}, RUN: {run_id}")

    # TODO: Check if all previous nodes have finished

    with worker_session() as db:
        job = models.pipeline.PipelineJob(pipeline_run_id=run_id, pipeline_node_id=node_id, status='Created')
        job.save(db)
        job.detach(db)

        # TODO: Locking
        if not previous_job_id:
            shutil.copytree('C:\\Users\\Adam\\Programming\\picom\\examples\\input', job.to_abs_path(job.input_path), dirs_exist_ok=True)
        else:
            prev_job = db.query(models.pipeline.PipelineJob).get(previous_job_id)
            shutil.copytree(prev_job.to_abs_path(prev_job.output_path), job.to_abs_path(job.input_path), dirs_exist_ok=True)

        volumes = {
            job.to_abs_path(job.input_path): {'bind': config.PICOM_INPUT_DIR, 'mode': 'ro'},
            job.to_abs_path(job.output_path): {'bind': config.PICOM_OUTPUT_DIR, 'mode': 'rw'}
        }

    container: Container = client.containers.run('picom_example_container', detach=True, volumes=volumes, remove=True)
    with worker_session() as db:
        job.status = 'running'
        job.save(db)

    # Long running task
    print('Waiting for container')
    # TODO: add spin wait
    exit_code = container.wait()['StatusCode']
    print('Container finished with exit code', exit_code)
    with worker_session() as db:
        job.status = 'exited'
        job.exit_code = exit_code
        job.save(db)

        if exit_code != 0:
            container.reload()
            stderr = container.logs(stdout=False, stderr=True).decode("utf-8")
            job_error = models.pipeline.PipelineJobError(pipeline_job_id=job.id, stderr=stderr)
            job_error.save(db)
        elif job.node.is_leaf_node():
            # TODO: Handle multiple lead nodes
            pass
        else:
            next_nodes = job.node.get_next_nodes()
            [run_node(run_id, n.id, job.id) for n in next_nodes]


def run_pipeline(folder: str, pipeline_id: int):
    with worker_session() as db:
        pipeline = db.query(models.pipeline.Pipeline).get(pipeline_id)
        starting_nodes = pipeline.get_starting_nodes()

        run = models.pipeline.PipelineRun(status='running').save(db)
        db.commit()

        [run_node(run.id, n.id) for n in starting_nodes]


if __name__ == '__main__':
    build_container(2)
    run_pipeline('xyz', 1)
