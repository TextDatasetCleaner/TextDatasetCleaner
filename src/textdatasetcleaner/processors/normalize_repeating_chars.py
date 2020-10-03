import string
from pathlib import Path
from typing import Optional

from textacy.preprocessing import normalize_repeating_chars

from .base import BaseProcessor


# prevent remove '...'
PUNCTUATION_MAP = string.punctuation.replace('.', '')
# FIXME: error in slash escaping inside of `normalize_repeating_chars` func
#        maybe already fixed in textacy?
PUNCTUATION_MAP = PUNCTUATION_MAP.replace('\\', '')


class NormalizeRepeatingCharsProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        for punct in PUNCTUATION_MAP:
            if punct in line:
                line = normalize_repeating_chars(line, chars=punct, maxn=1)
        if '....' in line:
            line = normalize_repeating_chars(line, chars='.', maxn=3)

        return line
