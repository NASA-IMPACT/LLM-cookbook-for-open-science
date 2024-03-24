import os


def path_exists(path):
    """Check if path exists. print error if not"""
    path_exist = os.path.exists(path)
    if not path_exists:
        print(f"Path does not exist: {path}")
    return path_exist
