from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, Session
from inflection import underscore

engine = create_engine(config.POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


class BaseModel(object):
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(self):
        return underscore(self.__name__)

    def save(self, session: Session):
        session.add(self)
        self._flush(session)
        return self

    def delete(self, session: Session):
        session.delete(self)
        self._flush(session)

    # noinspection PyMethodMayBeStatic
    def _flush(self, session: Session):
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise


BaseModel = declarative_base(cls=BaseModel)

