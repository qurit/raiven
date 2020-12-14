from tests import client, testing_session, utils, TEST_USER, schemas


def test_get_stats(authorization_header):
    response = client.get('/pipeline/stats')
    assert response.status_code == 401

    response = client.get('/pipeline/stats', headers=authorization_header)
    assert response.status_code == 200


def test_get_runs_graph(authorization_header):
    response = client.get('/pipeline/runs', headers=authorization_header)
    assert response.status_code == 200


def test_get_results(authorization_header):
    response = client.get('/pipeline/results', headers=authorization_header)
    assert response.status_code == 200


# TODO:
def test_download_run():
    raise NotImplementedError


def test_download_run_dne(authorization_header):
    response = client.get('/pipeline/download/', headers=authorization_header)
    assert response.status_code != 200

    response = client.get('/pipeline/download/-1', headers=authorization_header)
    assert response.status_code == 404

    response = client.get('/pipeline/download/0', headers=authorization_header)
    assert response.status_code == 404


# TODO:
def test_download_run_another_users():
    raise NotImplementedError


def test_get_all_pipelines(authorization_header):
    response = client.get('/pipeline/', headers=authorization_header)
    assert response.status_code == 200
    assert type(response.json()) is list

    return response.json()


def test_create_pipeline(authorization_header, pipeline = schemas.pipeline.PipelineCreate(name='test-pipeline')):
    # Create
    before = test_get_all_pipelines(authorization_header)
    response = client.post('/pipeline/', headers=authorization_header, json=pipeline.dict())
    data = response.json()
    after = test_get_all_pipelines(authorization_header)

    assert response.status_code == 200
    assert len(after) == len(before) + 1
    assert data['name'] == pipeline.name

    response = client.get(f'/pipeline/{data["id"]}', headers=authorization_header)
    assert response.status_code == 200

    return response.json()


def test_update_pipeline(authorization_header):
    pipeline = schemas.pipeline.PipelineCreate(name='test-update')
    pipeline_id = test_create_pipeline(authorization_header, pipeline)['id']

    assert pipeline_id
    raise NotImplementedError


def test_delete_pipeline(authorization_header):
    pipeline = schemas.pipeline.PipelineCreate(name='test-delete')
    pipeline_id = test_create_pipeline(authorization_header, pipeline)['id']
    assert pipeline_id

    response = client.delete(f'/pipeline/{pipeline_id}', headers=authorization_header)
    assert response.status_code == 200

    response = client.get(f'/pipeline/{pipeline_id}', headers=authorization_header)
    assert response.status_code == 404


def test_delete_pipeline_dne(authorization_header):
    pipeline = schemas.pipeline.PipelineCreate(name='test-delete-dne')
    pipeline_id = test_create_pipeline(authorization_header, pipeline)['id']
    assert pipeline_id

    response = client.delete(f'/pipeline/{pipeline_id}', headers=authorization_header)
    assert response.status_code == 200

    response = client.delete(f'/pipeline/{pipeline_id}', headers=authorization_header)
    assert response.status_code == 404
