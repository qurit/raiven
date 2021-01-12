import os
import pytest
from api.models.pipeline import Pipeline, PipelineRun
from tests import config

from api.pipelining._control import DicomIngestController
from tests.test_models.test_pipelines import insert_pipeline


def test_ingest_with_bad_ae_title(mock_images_folder):
    # TODO update test when edge case is implemented
    with pytest.raises(NotImplementedError):
        DicomIngestController(mock_images_folder, "test", "test", "0", "BAD_AET")


def test_ingest_folder_to_bad_pipeline(mock_images_folder):
    # TODO update test when edge case is implemented
    with pytest.raises(NotImplementedError):
        assert not DicomIngestController(mock_images_folder, "test", "test", "0", config.PIPELINE_AE_PREFIX + "non-existant-ae")


def test_ingest_folder_to_valid_pipeline(mock_images_folder, db):
    # Insert pipeline to be run
    ae_title = 'test_ingest'
    insert_pipeline(db, "test", ae_title=ae_title)

    # Test the pipeline was run
    init_pipeline_run_count = db.query(PipelineRun).count()
    assert DicomIngestController(mock_images_folder, "test", "test", "0", config.PIPELINE_AE_PREFIX + ae_title)
    assert init_pipeline_run_count < db.query(PipelineRun).count()
    assert not os.path.exists(mock_images_folder.resolve()) # Temp folder gets removed on delete
    
