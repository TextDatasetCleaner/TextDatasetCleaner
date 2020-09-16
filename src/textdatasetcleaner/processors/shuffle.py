from .base import BaseProcessor


class ShuffleProcessor(BaseProcessor):

    __processor_name__ = 'shuffle'
    __processor_type__ = 'file'

    def process_file(self, file_path: str) -> bool:
        pass
