from pathlib import Path
from typing import Optional

from textacy.preprocessing.resources import RE_PHONE_NUMBER

from textdatasetcleaner.exceptions import TDCValueError
from textdatasetcleaner.processors.base import BaseProcessor


class FilterPhoneNumberProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, mode: str = 'remove_line', replace_with: str = ' '):
        allowed = ['remove_line', 'replace']
        if mode not in allowed:
            raise TDCValueError(f'Wrong mode for {self.name} processor: {mode}, allowed only: {allowed}')

        self.mode = mode
        self.replace_with = replace_with

    def process_line(self, line: str) -> Optional[str]:
        if self.mode == 'remove_line':
            if RE_PHONE_NUMBER.search(line):
                return None

        elif self.mode == 'replace':
            # TODO: bench 'sub' vs 'search + sub'
            line = RE_PHONE_NUMBER.sub(self.replace_with, line)

        return line
