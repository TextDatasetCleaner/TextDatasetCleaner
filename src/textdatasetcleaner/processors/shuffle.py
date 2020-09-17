from .base import BaseProcessor


class ShuffleProcessor(BaseProcessor):

    __processor_name__ = 'shuffle'
    __processor_type__ = 'file'

    def process_file(self, input_file: str, output_file: str) -> bool:
        return True
