from pathlib import Path
from typing import Optional

from textdatasetcleaner.processors.base import BaseProcessor


class LineStripProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        return line.strip()
