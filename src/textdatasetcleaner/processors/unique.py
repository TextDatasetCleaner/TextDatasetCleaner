import subprocess  # noqa: S404
from pathlib import Path

from textdatasetcleaner.helpers import find_command_path
from textdatasetcleaner.processors.base import BaseProcessor


class UniqueProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'file'

    # TODO: add timeout in __init__
    def __init__(self) -> None:
        self.sort_cmd_path = find_command_path('sort')
        self.uniq_cmd_path = find_command_path('uniq')

    def process_file(self, input_file: str, output_file: str) -> bool:
        # BSD sort + uniq very fast

        with open(output_file, 'w', encoding='utf-8') as fdw:
            p1 = subprocess.Popen([self.sort_cmd_path, input_file], stdout=subprocess.PIPE)
            p2 = subprocess.Popen([self.uniq_cmd_path], stdin=p1.stdout, stdout=fdw)
            p1.wait()
            p2.communicate()

        return p1.returncode == 0 and p2.returncode == 0
