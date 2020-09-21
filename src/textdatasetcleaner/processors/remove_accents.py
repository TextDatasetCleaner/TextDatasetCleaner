from pathlib import Path
from typing import Optional

from textacy.preprocessing import remove_accents

from .base import BaseProcessor


class RemoveAccentsProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        line = remove_accents(line)

        return line
