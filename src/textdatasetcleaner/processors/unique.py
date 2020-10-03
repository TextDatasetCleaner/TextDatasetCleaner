import subprocess
from pathlib import Path

from .base import BaseProcessor


class UniqueProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'file'

    # TODO: add timeout in __init__

    def process_file(self, input_file: str, output_file: str) -> bool:
        # BSD sort + uniq very fast

        with open(output_file, 'w', encoding='utf-8') as fdw:
            p1 = subprocess.Popen(['sort', input_file], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(['uniq'], stdin=p1.stdout, stdout=fdw)
            p1.stdout.close()
            p2.communicate()
            p1.wait()

        return p1.returncode == 0 and p2.returncode == 0
