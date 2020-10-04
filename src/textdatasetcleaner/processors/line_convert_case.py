from pathlib import Path
from typing import Optional

from textdatasetcleaner.exceptions import TDCValueError
from textdatasetcleaner.processors.base import BaseProcessor


class LineConvertCaseProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, mode: str):
        allowed = ['title', 'lower', 'upper']
        if mode not in allowed:
            raise TDCValueError(f'Wrong mode for {self.name} processor: {mode}, allowed only: {allowed}')
        self.mode = mode

    def process_line(self, line: str) -> Optional[str]:
        return getattr(line, self.mode)()
