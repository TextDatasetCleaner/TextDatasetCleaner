from pathlib import Path
from typing import Optional

from textacy.preprocessing.resources import RE_CURRENCY_SYMBOL

from .base import BaseProcessor


class FilterCurrencySymbolsProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, mode: str = 'remove_line', replace_to: str = ' '):
        allowed = ['remove_line', 'replace']
        if mode not in allowed:
            # TODO: own exc
            raise ValueError(f'Wrong mode for {self.name} processor: {mode}, allowed only: {allowed}')

        self.mode = mode
        self.replace_to = replace_to

    def process_line(self, line: str) -> Optional[str]:
        if self.mode == 'remove_line':
            if RE_CURRENCY_SYMBOL.search(line):
                return None

        elif self.mode == 'replace':
            # TODO: bench 'sub' vs 'search + sub'
            line = RE_CURRENCY_SYMBOL.sub(self.replace_to, line)

        return line
