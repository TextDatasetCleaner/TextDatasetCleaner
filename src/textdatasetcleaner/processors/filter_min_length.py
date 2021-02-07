from pathlib import Path
from typing import Optional

from textdatasetcleaner.helpers import get_line_piece
from textdatasetcleaner.processors.base import BaseProcessor


class FilterMinLengthProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, threshold: int, delimiter: Optional[str] = None, delimited_position: int = -1):
        self.threshold = threshold

        self.delimiter = delimiter
        self.delimited_position = delimited_position

    def process_line(self, line: str) -> Optional[str]:
        line_cpy = get_line_piece(line, self.delimiter, self.delimited_position)

        if len(line_cpy) < self.threshold:
            return None

        return line
