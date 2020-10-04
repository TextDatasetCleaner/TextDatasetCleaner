from pathlib import Path
from typing import Optional

from profanity_check import predict_prob  # type: ignore

from textdatasetcleaner.processors.base import BaseProcessor


class RemoveProfanityProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, threshold: float = 0.9):
        self.threshold = threshold

    def process_line(self, line: str) -> Optional[str]:
        if predict_prob([line])[0] > self.threshold:
            return None

        return line
