import os
import shutil

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ['UNIT_TESTING'] = 'True'
os.environ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./test.db?check_same_thread=False"
os.environ['UPLOAD_DIR'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_uploads')

from api import app, models, config, schemas
from api.database import worker_session as testing_session


client = TestClient(app)

TEST_USER = schemas.user.UserLocalCreate(
    username='test_user',
    name='Test User',
    password='pAssWord'
)
