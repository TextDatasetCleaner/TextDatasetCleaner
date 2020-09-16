from typing import Optional

from .base import BaseProcessor


class LineStripProcessor(BaseProcessor):

    __processor_name__ = 'line_strip'
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        line = line.strip()
        if not line:
            return None

        return line
