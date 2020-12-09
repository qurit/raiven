import pathlib
import pytest

from tests import models


class TestModel(models.Base, models.IOPathMixin):
    pass


def test_io_path_mixin_not_yet_saved():
    mixin = TestModel()

    with pytest.raises(Exception):
        mixin.get_abs_path()

    with pytest.raises(Exception):
        mixin.get_abs_output_path()


if __name__ == '__main__':
    test_io_path_mixin()