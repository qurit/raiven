import pathlib

from api.models.pipeline import *

from tests import utils


def insert_pipeline(db, name, **kwargs) -> Pipeline:
    user = utils.get_test_user(db)
    pipeline = Pipeline(user_id=user.id, name=name, **kwargs)
    pipeline.save(db)
    db.commit()

    assert pipeline.id
    assert pipeline.user_id

    return pipeline


def insert_run(db, pipeline, **kwargs) -> PipelineRun:
    run = PipelineRun(pipeline_id=pipeline.id, **kwargs)
    run.save(db)
    db.commit()

    assert run.id
    assert run.pipeline_id

    return run


def insert_job(db, run, **kwargs) -> PipelineJob:
    job = PipelineJob(pipeline_run_id=run.id, **kwargs)
    job.save(db)
    db.commit()

    assert job.id
    assert job.pipeline_run_id

    return job


def test_pipeline_model(db):
    pipeline = insert_pipeline(db, 'test')

    assert not pipeline.runs
    assert not pipeline.nodes
    assert not pipeline.links
    assert type(pipeline.get_starting_nodes()) is list and not pipeline.get_starting_nodes()

    pipeline.delete(db)
    db.commit()


def test_pipeline_run(db):
    pipeline = insert_pipeline(db, 'Test Pipeline run')
    run = insert_run(db, pipeline)

    assert os.path.exists(run_path := run.get_abs_path())
    assert os.path.isdir(run_path)

    run.delete(db)
    assert not os.path.exists(run_path)

    db.commit()


def test_pipeline_job(db):
    pipeline = insert_pipeline(db, 'Test Pipeline job')
    run = insert_run(db, pipeline)
    job = insert_job(db, run)

    assert os.path.exists(job_path := job.get_abs_path())
    assert os.path.isdir(job_path)

    job.delete(db)
    assert not os.path.exists(job_path)

    db.commit()


# noinspection DuplicatedCode
def test_cascade_delete_pipeline(db):
    pipeline = insert_pipeline(db, 'Test Pipeline Delete 1')
    run = insert_run(db, pipeline)
    job = insert_job(db, run)

    run_path = run.get_abs_path()
    job_path = job.get_abs_path()

    assert os.path.exists(run_path)
    assert os.path.exists(job_path)

    pipeline.delete(db)
    db.commit()

    assert not PipelineRun.query(db).get(run.id)
    assert not PipelineJob.query(db).get(job.id)

    assert not os.path.exists(run_path)
    assert not os.path.exists(job_path)


# noinspection DuplicatedCode
def test_cascade_delete_run(db):
    pipeline = insert_pipeline(db, 'Test Pipeline Delete 2')
    run = insert_run(db, pipeline)
    job = insert_job(db, run)

    run_path = run.get_abs_path()
    job_path = job.get_abs_path()

    assert os.path.exists(run_path)
    assert os.path.exists(job_path)

    run.delete(db)
    db.commit()

    assert Pipeline.query(db).get(pipeline.id)
    assert not PipelineRun.query(db).get(run.id)
    assert not PipelineJob.query(db).get(job.id)

    assert not os.path.exists(run_path)
    assert not os.path.exists(job_path)


def test_job_volumes_paths(db):
    pipeline = insert_pipeline(db, 'Test Pipeline Delete 2')
    run = insert_run(db, pipeline)
    job = insert_job(db, run)

    in_v = str(job.get_volume_abs_input_path())
    out_v = str(job.get_volume_abs_output_path())

    assert os.path.exists(in_v)
    assert os.path.exists(out_v)

    # Making sure the paths are not windows paths and linux paths
    assert not ('\\' in in_v and '/' in in_v)
    assert not ('\\' in out_v and '/' in out_v)


def test_linux_paths(db):
    pipeline = insert_pipeline(db, 'Test Pipeline Delete 2')
    run = insert_run(db, pipeline)
    job = insert_job(db, run)

    assert '\\' not in run.input_path
    assert '\\' not in run.output_path
    assert pathlib.Path(run.input_path).as_posix() == run.input_path
    assert pathlib.Path(run.output_path).as_posix() == run.output_path

    assert '\\' not in job.input_path
    assert '\\' not in job.output_path
    assert pathlib.Path(job.input_path).as_posix() == job.input_path
    assert pathlib.Path(job.output_path).as_posix() == job.output_path
