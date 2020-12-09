import pathlib
import posixpath
import pytest

from tests import models, testing_session


def test_nested_path_mixin_not_saved():
    class TestNestedPathModel(models.Base, models.NestedPathMixin):
        pass

    mixin = TestNestedPathModel()

    with pytest.raises(NotImplementedError):
        mixin.get_abs_path()

    with pytest.raises(NotImplementedError):
        mixin.get_path()


def test_io_path_mixin_saved():
    class TestIOModel(models.Base, models.IOPathMixin):
        pass

    mixin = TestIOModel()

    with pytest.raises(Exception):
        mixin.get_abs_path()

    with pytest.raises(Exception):
        mixin.get_abs_output_path()

#
# def test_nested_path_mixin():
#     assert issubclass(models.container.Container,  models.NestedPathMixin)
#
#     with testing_session() as db:
#         db_container = db.query(models.container.Container).first()
#         assert db_container
#
#         assert pathlib.Path(db_container.get_abs_path()).exists()
#
#         # TODO: GET THIS TEST TO PASS
#         # assert db_container.get_path() == pathlib.Path(db_container.get_path()).as_posix()
