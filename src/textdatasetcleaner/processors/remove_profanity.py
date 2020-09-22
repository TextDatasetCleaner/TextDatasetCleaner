from typing import Optional
from pathlib import Path

from profanity_check import predict_prob

from .base import BaseProcessor


class RemoveProfanityProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, threshold: float = 0.9):
        self.threshold = threshold

    def process_line(self, line: str) -> Optional[str]:
        if predict_prob([line])[0] > self.threshold:
            return None

        return line
