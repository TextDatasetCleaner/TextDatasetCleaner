from pathlib import Path
from typing import Optional

from textacy.preprocessing import normalize_unicode  # type: ignore

from textdatasetcleaner.exceptions import TDCValueError
from textdatasetcleaner.processors.base import BaseProcessor


class NormalizeUnicodeProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, form: str = 'NFKC'):
        allowed = ['NFC', 'NFD', 'NFKC', 'NFKD']
        if form not in allowed:
            raise TDCValueError(f'Wrong form for {self.name} processor: {form}, allowed only: {allowed}')

        self.form = form

    def process_line(self, line: str) -> Optional[str]:
        return normalize_unicode(line, form=self.form)
