import os
import shutil
import docker
from api import config, worker_session, models

client = docker.from_env()


def run_node(run_id: int, node_id: int, previous_job_id: int = None):
    print(f"RUNNING NODE: {node_id}, RUN: {run_id}")

    with worker_session() as db:
        job = models.pipeline.PipelineJob(pipeline_run_id=run_id, pipeline_node_id=node_id, status='Created')
        job.save(db)
        job.detach(db)

    # TODO: Locking
    if not previous_job_id:
        shutil.copytree('C:\\Users\\Adam\\Programming\\picom\\examples\\input', job.to_abs_path(job.input_path), dirs_exist_ok=True)
    else:
        # TODO: COPY files from previous job
        pass

    volumes = {
        job.to_abs_path(job.input_path): {'bind': config.PICOM_INPUT_DIR, 'mode': 'ro'},
        job.to_abs_path(job.output_path): {'bind': config.PICOM_OUTPUT_DIR, 'mode': 'ro'}
    }

    container: Container = client.containers.run('picom_example_container', detach=True, volumes=volumes)
    with worker_session() as db:
        job.status = 'running'
        job.save(db)
        job.detach(db)

    # Long running task
    exit_code = container.wait()['StatusCode']

    with worker_session() as db:
        job.status = 'exited'
        job.exit_code = exit_code
        job.save(db)

        if exit_code != 0:
            container.reload()
            stderr = container.logs(stdout=False, stderr=True).decode("utf-8")
            job_error = models.pipeline.PipelineJobError(pipeline_job_id=job.id, stderr=stderr)
            job_error.save(db)


def run_pipeline(folder: str, pipeline_id: int):
    with worker_session() as db:
        pipeline = db.query(models.pipeline.Pipeline).get(pipeline_id)
        starting_nodes = pipeline.get_starting_nodes()

        run = models.pipeline.PipelineRun().save(db)
        db.commit()

        [run_node(run.id, n.id) for n in starting_nodes]


if __name__ == '__main__':
    run_pipeline('xyz', 1)
