from typing import Optional
from pathlib import Path

from selectolax.parser import HTMLParser

from .base import BaseProcessor


class CleanHTMLProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, or_condition: bool = False):
        self.or_condition = or_condition

    def process_line(self, line: str) -> Optional[str]:
        if self.or_condition:
            checker = '<' in line or '>' in line
        else:
            checker = '<' in line and '>' in line

        if checker:
            tree = HTMLParser(line)
            line = tree.body.text(separator=' ')
            line = line.strip()

        return line
