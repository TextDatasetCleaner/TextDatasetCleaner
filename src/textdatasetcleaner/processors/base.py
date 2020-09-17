from abc import ABC
from typing import Optional

from ..helpers import ClassProperty


class BaseProcessor(ABC):
    __processor_name__ = ''
    __processor_type__ = ''

    def process_line(self, line: str) -> Optional[str]:
        """
            @:returns: None if need skip this line
        """
        raise NotImplemented()

    def process_file(self, input_file: str, output_file: str) -> bool:
        raise NotImplemented()

    @ClassProperty
    def name(self):
        return self.__processor_name__

    @ClassProperty
    def type(self):
        return self.__processor_type__
