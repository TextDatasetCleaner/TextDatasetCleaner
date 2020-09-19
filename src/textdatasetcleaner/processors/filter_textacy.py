import string
from pathlib import Path
from typing import Optional

from textacy.preprocessing import (
    normalize_hyphenated_words,
    normalize_quotation_marks,
    normalize_repeating_chars,
    normalize_unicode,
    normalize_whitespace,
    remove_accents,
)
from textacy.preprocessing.resources import (
    RE_EMAIL,
    RE_SHORT_URL,
    RE_URL,
)

from .base import BaseProcessor


# prevent remove '...'
PUNCTUATION_MAP = string.punctuation.replace('.', '')
# FIXME: error in slash escaping inside of normalize_repeating_chars
#        maybe already fixed in textacy?
PUNCTUATION_MAP = PUNCTUATION_MAP.replace('\\', '')


class FilterTextacyProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, or_condition: bool = False):
        self.or_condition = or_condition

    def process_line(self, line: str) -> Optional[str]:
        # TODO: maybe remove urls / emails, not skip?
        if RE_SHORT_URL.search(line):
            return None
        if RE_URL.search(line):
            return None
        if RE_EMAIL.search(line):
            return None

        # fixes and normalization
        line = remove_accents(line)
        line = normalize_hyphenated_words(line)
        line = normalize_quotation_marks(line)
        line = normalize_unicode(line, form='NFKC')

        # repeating symbols
        for punct in PUNCTUATION_MAP:
            if punct in line:
                line = normalize_repeating_chars(line, chars=punct, maxn=1)
        if '....' in line:
            line = normalize_repeating_chars(line, chars='.', maxn=3)

        # need be last
        line = normalize_whitespace(line)

        return line
