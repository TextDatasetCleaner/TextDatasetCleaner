import subprocess  # noqa: S404
from pathlib import Path

from textdatasetcleaner.helpers import find_command_path
from textdatasetcleaner.processors.base import BaseProcessor


class ShuffleProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'file'

    # TODO: add timeout in __init__
    def __init__(self) -> None:
        self.shuf_cmd_path = find_command_path('shuf')

    def process_file(self, input_file: str, output_file: str) -> bool:
        # GNU shuf very fast

        with open(input_file, encoding='utf-8') as fdr:
            p1 = subprocess.Popen([self.shuf_cmd_path, '-o', output_file], stdin=fdr)
            p1.communicate()

        return p1.returncode == 0
