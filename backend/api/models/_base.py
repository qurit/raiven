import os
from shutil import rmtree

from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session
from inflection import underscore, pluralize

from api import config


class _Base:
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


Base = declarative_base(cls=_Base)


class NestedPathMixin(object):

    @property
    def path(self) -> str:
        raise NotImplementedError

    @property
    def abs_path(self) -> str:
        return os.path.join(config.UPLOAD_DIR, self.path)


    def save(self, *args, **kwargs):
        """ Will Create a new directory upon completion """

        super().save(*args, **kwargs)
        if not os.path.exists(path := self.path):
            os.makedirs(path)

    def delete(self, *args, **kwargs):
        """ Will Delete a new directory upon completion """

        super().delete(*args, **kwargs)
        if os.path.exists(path := self.path):
            rmtree(path)


class PathMixin(NestedPathMixin):

    @declared_attr
    def __directory__(self) -> str:
        """ The naming scheme for the folder containing all the objects """

        return pluralize(self.__tablename__)

    @declared_attr
    def __absolute_directory__(self) -> str:
        return os.path.join(config.UPLOAD_DIR, self.__directory__)

    @property
    def path(self) -> str:
        return os.path.join(self.__directory__, str(self.id))
