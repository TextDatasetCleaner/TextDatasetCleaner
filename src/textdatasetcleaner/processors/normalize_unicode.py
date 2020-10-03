from pathlib import Path
from typing import Optional

from textacy.preprocessing import normalize_unicode

from .base import BaseProcessor
from ..exceptions import TDSValueError


class NormalizeUnicodeProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, form: str = 'NFKC'):
        allowed = ['NFC', 'NFD', 'NFKC', 'NFKD']
        if form not in allowed:
            raise TDSValueError(f'Wrong form for {self.name} processor: {form}, allowed only: {allowed}')

        self.form = form

    def process_line(self, line: str) -> Optional[str]:
        line = normalize_unicode(line, form=self.form)

        return line
