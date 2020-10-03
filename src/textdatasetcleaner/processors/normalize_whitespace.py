from pathlib import Path
from typing import Optional

from textacy.preprocessing import normalize_whitespace

from .base import BaseProcessor


class NormalizeWhitespaceProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        line = normalize_whitespace(line)

        return line
