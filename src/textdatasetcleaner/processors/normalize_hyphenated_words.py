from pathlib import Path
from typing import Optional

from textacy.preprocessing import normalize_hyphenated_words  # type: ignore

from textdatasetcleaner.processors.base import BaseProcessor


class NormalizeHyphenatedWordsProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        return normalize_hyphenated_words(line)
