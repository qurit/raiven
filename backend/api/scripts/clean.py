import pathlib
import shutil

from api import config

from api.models.container import Container
from api.models.dicom import DicomNode
from api.models.pipeline import PipelineJob, PipelineRun, PipelineNodeStorageBucket

MODELS = [Container, DicomNode, PipelineJob, PipelineRun, PipelineNodeStorageBucket]


def cleanup_folders(db):
    for model in MODELS:
        folder = pathlib.Path(config.UPLOAD_DIR) / model.__directory__

        if not folder.exists():
            continue

        for file in folder.iterdir():
            if file.is_dir() and not db.query(model).get(file.stem):
                shutil.rmtree(file)
