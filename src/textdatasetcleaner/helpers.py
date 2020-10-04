import os
import tempfile
from typing import Optional

import requests
import yaml

from textdatasetcleaner.exceptions import TDCValueError

CHUNK_SIZE = 16384


def load_config(path: str):
    with open(path) as fd:
        return yaml.safe_load(fd)


def get_line_piece(line: str, delimiter: Optional[str], delimited_position: int):
    if delimiter is not None:
        pos = line.find(delimiter)
        if pos != -1:
            line = line.split(delimiter)[delimited_position]

    return line


def download_file(url: str, save_path: str):
    response = requests.get(url, stream=True)

    if not response.ok:
        raise TDCValueError(f'Download {url} failed with code {response.status_code}')

    # TODO: log download started / finished
    with open(save_path, 'wb') as fh:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            fh.write(chunk)

    # TODO: checksum validation?


def get_temp_file_path(config=None) -> str:
    if config is None:
        config = {}

    cache_dir: str = ''
    if 'CACHE_DIR' in config:
        cache_dir = config.get('CACHE_DIR', '')
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

    if not cache_dir:
        temp_dir = None
    else:
        temp_dir = cache_dir

    _, temp_file_path = tempfile.mkstemp(dir=temp_dir)

    return temp_file_path


# TODO: disable setter or find better method
class ClassProperty(object):

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner):
        return self.func(owner)
