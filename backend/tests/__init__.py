import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# os.environ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./test.db"

from api import app, models, config
from api.database import worker_session as testing_session


client = TestClient(app)
