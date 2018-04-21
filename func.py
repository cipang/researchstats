import os


def get_data_file_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "data", filename)
