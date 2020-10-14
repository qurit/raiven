import docker
from api import config, worker_session, models


def run_node(db, run_id: int, node_id: int, previous_job_id: int = None):
    print(f"RUNNING NODE: {node_id}, RUN: {run_id}")

    job = models.pipeline.PipelineJob(
        pipeline_run_id=run_id,
        pipeline_node_id=node_id,
        status='Created',
    ).save(db)


def run_pipeline(folder: str, pipeline_id: int):
    with worker_session() as db:
        pipeline = db.query(models.pipeline.Pipeline).get(pipeline_id)
        starting_nodes = pipeline.get_starting_nodes()

        run = models.pipeline.PipelineRun().save(db)

        [run_node(db, run.id, n.id) for n in starting_nodes]

# client = docker.from_env()

if __name__ == '__main__':
    run_pipeline('xyz', 1)
