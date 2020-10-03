from pathlib import Path
from typing import Optional

from textacy.preprocessing import normalize_quotation_marks


from .base import BaseProcessor


class NormalizeQuotationMarksProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        line = normalize_quotation_marks(line)

        return line
