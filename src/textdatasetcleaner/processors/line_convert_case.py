from typing import Optional
from pathlib import Path

from .base import BaseProcessor


class LineConvertCaseProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, mode: str):
        allowed = ['title', 'lower', 'upper']
        if mode not in allowed:
            # TODO: own exc
            raise ValueError(f'Wrong mode for {self.name} processor: {mode}, allowed only: {allowed}')
        self.mode = mode

    def process_line(self, line: str) -> Optional[str]:
        line = getattr(line, self.mode)()

        return line
