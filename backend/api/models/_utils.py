from shutil import copytree

from . import NestedPathMixin, IOPathMixin


def copy_model_fs(src: NestedPathMixin, dst: IOPathMixin, dst_subdir='input'):
    """
    This function can be used to copy a model underlying folder (eg: a input or output folder) to the underlying folder
    of another model
    """

    if type(src) is IOPathMixin:
        src_dir = src.get_abs_output_path()
    else:
        src_dir = src.get_abs_path()

    if dst_subdir not in ['input', 'output']:
        ValueError('output_subdir kwarg can only be "input" or "output"')
    dst_dir = dst.get_abs_input_path() if dst_subdir == 'input' else dst.get_abs_output_path()

    # TODO: LOCKING ?
    copytree(src_dir, dst_dir, dirs_exist_ok=True, )
