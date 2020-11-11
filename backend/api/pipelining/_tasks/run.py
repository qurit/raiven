from api import config, worker_session, models
from . import docker


def run_node_task(run_id: int, node_id: int, previous_job_id: int = None):
    print(f"RUNNING NODE: {node_id}, RUN: {run_id}")

    # TODO: Check if all previous nodes have finished

    with worker_session() as db:
        job = models.pipeline.PipelineJob(pipeline_run_id=run_id, pipeline_node_id=node_id, status='Created')
        job.save(db)

        if not (build := job.node.container.build):
            # TODO: ABORT AND BUILD
            print('Cant run node because container is not built')
            return

        image_tag = build.tag
        job.detach(db)

        if not previous_job_id:
            src_subdir = 'input'
            prev = db.query(models.pipeline.PipelineRun).get(run_id)
        else:
            src_subdir = 'output'
            prev = db.query(models.pipeline.PipelineJob).get(previous_job_id)

        # TODO: Locking

        models.utils.copy_model_fs(prev, job, src_subdir=src_subdir)
        volumes = {
            job.get_abs_input_path(): {'bind': config.PICOM_INPUT_DIR, 'mode': 'ro'},
            job.get_abs_output_path(): {'bind': config.PICOM_OUTPUT_DIR, 'mode': 'rw'}
        }

    container: Container = docker.containers.run(image_tag, detach=True, volumes=volumes, labels=['Raiven'])
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

            # Run Complete
            run = db.query(models.pipeline.PipelineRun).get(run_id)
            models.utils.copy_model_fs(job, run, dst_subdir='output')
            run.status = 'complete'
            run.save(db)

            # TODO: Clean up old jobs
        else:
            next_nodes = job.node.get_next_nodes()
            [run_node(run_id, n.id, job.id) for n in next_nodes]

    # Cleaning Up Container
    container.remove()


def run_pipeline(pipeline_run_id: models.pipeline.PipelineRun):
    with worker_session() as db:
        run = models.pipeline.PipelineRun.query(db).get(pipeline_run_id)
        starting_nodes = run.pipeline.get_starting_nodes()

        run.status = 'running'
        run.save(db)
        db.commit()

        for node in starting_nodes:
            if not (build := node.container.build) or not build.is_success:
                # TODO: Build containers here if they haven't already been built
                print("TODO: some containers need to be built. Exiting")
                return

        [run_node(run.id, n.id) for n in starting_nodes]