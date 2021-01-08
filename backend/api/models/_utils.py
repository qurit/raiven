import pathlib
from shutil import copytree

from . import NestedPathMixin, IOPathMixin


def copy_model_fs(src: NestedPathMixin, dst: IOPathMixin, dst_subdir='input', src_subdir='output'):
    """
    This function can be used to copy a model underlying folder (eg: a input or output folder) to the underlying folder
    of another model
    """
    if src_subdir not in ['input', 'output']:
        ValueError('src_subdir kwarg can only be "input" or "output"')
    if dst_subdir not in ['input', 'output']:
        ValueError('dst_subdir kwarg can only be "input" or "output"')

    src_dir = pathlib.Path(src.get_abs_path(subdir=src_subdir)).resolve()
    dst_dir = pathlib.Path(dst.get_abs_path(subdir=dst_subdir)).resolve()

    copytree(src_dir, dst_dir, dirs_exist_ok=True)
