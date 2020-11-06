from pathlib import Path
from typing import Optional

from textdatasetcleaner.processors.base import BaseProcessor


class AddPostfixProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, text: str):
        self.text = text

    def process_line(self, line: str) -> Optional[str]:
        return f'{line}{self.text}'
