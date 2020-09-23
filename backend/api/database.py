from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from inflection import underscore

from api import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
