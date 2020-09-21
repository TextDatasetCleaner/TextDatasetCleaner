from typing import Optional
from pathlib import Path

from .base import BaseProcessor


class LineStripProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        line = line.strip()

        return line
