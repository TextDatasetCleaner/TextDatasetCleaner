from pathlib import Path

from .base import BaseProcessor


class ShuffleProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'file'

    def process_file(self, input_file: str, output_file: str) -> bool:
        return True
