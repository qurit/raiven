import pathlib
from datetime import datetime

from api import config, worker_session, models
from . import docker, dramatiq, external_sio, HOST_PATH_TYPE


@dramatiq.actor(max_retries=0)
def run_node_task(run_id: int, node_id: int, previous_job_id: int = None):
    # external_sio.emit('message', f"RUNNING NODE: {node_id}, RUN: {run_id}")
    print('Got past the emit')

    # TODO: Check if all previous nodes have finished

    with worker_session() as db:
        job = models.pipeline.PipelineJob(pipeline_run_id=run_id, pipeline_node_id=node_id, status='Created')
        job.save(db)

        if not (build := job.node.container.build):
            # TODO: ABORT AND BUILD
            print('Cant run node because container is not built')
            return

        image_tag = build.tag

        if not previous_job_id:
            src_subdir = 'input'
            prev = db.query(models.pipeline.PipelineRun).get(run_id)
        else:
            src_subdir = 'output'
            prev = db.query(models.pipeline.PipelineJob).get(previous_job_id)

        models.utils.copy_model_fs(prev, job, src_subdir=src_subdir)
        volumes = {
            HOST_PATH_TYPE(job.get_volume_abs_input_path()): {'bind': config.PICOM_INPUT_DIR, 'mode': 'ro'},
            HOST_PATH_TYPE(job.get_volume_abs_output_path()): {'bind': config.PICOM_OUTPUT_DIR, 'mode': 'rw'}
        }
        print(volumes)

    container: Container = docker.containers.run(
        image_tag, detach=True, volumes=volumes, labels=['Raiven'])
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
            job_error = models.pipeline.PipelineJobError(
                pipeline_job_id=job.id, stderr=stderr)
            job_error.save(db)
        elif job.node.is_leaf_node():
            # TODO: Handle multiple lead nodes

            # Run Complete
            run = db.query(models.pipeline.PipelineRun).get(run_id)
            models.utils.copy_model_fs(job, run, dst_subdir='output')
            run.status = 'complete'
            run.finished_datetime = datetime.now()
            run.save(db)

            print('emit pipeline finished')
            # external_sio.emit('message', f"PIPELINE FINISHED NODE")

            # TODO: Clean up old jobs
        else:
            next_nodes = job.node.get_next_nodes()
            [run_node_task.send_with_options(
                args=(run_id, n.id, job.id,)) for n in next_nodes]

    # Cleaning Up Container
    container.remove()
