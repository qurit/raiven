from sqlalchemy import Column, Integer
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from inflection import underscore


def init_db(db: Database):
    # Initializes the database. Adapted from Biodi.
    session = db.session

    class Base(object):
        id = Column(Integer, primary_key=True)

        @declared_attr
        def __tablename__(self):
            return underscore(self.__name__)

        def save(self):
            session.add(self)
            self._flush()
            return self

        def update(self, **kwargs):
            for attr, value in kwargs.items():
                setattr(self, attr, value)
            return self.save()

        def delete(self):
            session.delete(self)
            self._flush()

        # noinspection PyMethodMayBeStatic
        def _flush(self):
            try:
                session.flush()
            except DatabaseError:
                session.rollback()
                raise

    db.Model = declarative_base(cls=Base)
    db.Model.query = session.query_property()
    db.Model.metadata.create_all(bind=db.engine)
    db.create_all()
