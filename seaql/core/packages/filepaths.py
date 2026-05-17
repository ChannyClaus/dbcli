import os


def dir_path_exists(path):
    dir_name = os.path.dirname(path)
    return os.path.exists(dir_name) and os.path.isdir(dir_name)
