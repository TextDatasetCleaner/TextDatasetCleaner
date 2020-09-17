from typing import Optional

import yaml


def load_config(path: str):
    return yaml.safe_load(open(path))


def get_line_piece(line: str, delimiter: Optional[str], delimited_position: int):
    if delimiter is not None:
        pos = line.find(delimiter)
        if pos != -1:
            line = line.split(delimiter)[delimited_position]

    return line


# TODO: disable setter or find better method
class ClassProperty(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
