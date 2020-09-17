from .base import BaseProcessor


class UniqueProcessor(BaseProcessor):

    __processor_name__ = 'unique'
    __processor_type__ = 'file'

    def process_file(self, input_file: str, output_file: str) -> bool:
        pass
