import os
import tempfile
from typing import Optional

import requests
import yaml

from .exceptions import TDSValueError


def load_config(path: str):
    return yaml.safe_load(open(path))


def get_line_piece(line: str, delimiter: Optional[str], delimited_position: int):
    if delimiter is not None:
        pos = line.find(delimiter)
        if pos != -1:
            line = line.split(delimiter)[delimited_position]

    return line


def download_file(url: str, save_path: str):
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise TDSValueError(f'Download {url} failed with code {response.status_code}')

    # TODO: log download started / finished
    with open(save_path, 'wb') as fh:
        for chunk in response.iter_content(chunk_size=16 * 1024):
            fh.write(chunk)

    # TODO: checksum validation?


def get_temp_file_path(config=None):
    if config is None:
        config = dict()

    cache_dir: Optional[str] = None
    if 'CACHE_DIR' in config:
        cache_dir = config['CACHE_DIR']
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

    _, temp_file_path = tempfile.mkstemp(dir=cache_dir)

    return temp_file_path


# TODO: disable setter or find better method
class ClassProperty(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
