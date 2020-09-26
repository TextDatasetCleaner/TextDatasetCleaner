from abc import ABC
from typing import Optional

from ..helpers import ClassProperty
from ..exceptions import TDSNotImplemented


class BaseProcessor(ABC):

    __processor_name__ = None
    __processor_type__ = None

    def __init__(self, *args, **kwargs):
        pass

    def process_line(self, line: str) -> Optional[str]:
        """
            @:returns: None if need skip this line
        """
        raise TDSNotImplemented()

    def process_file(self, input_file: str, output_file: str) -> bool:
        raise TDSNotImplemented()

    @ClassProperty
    def name(self):
        if self.__processor_name__ is None:
            raise TDSNotImplemented('Processor name not overloaded!')
        return self.__processor_name__

    @ClassProperty
    def type(self):
        if self.__processor_type__ is None:
            raise TDSNotImplemented('Processor type not overloaded!')
        return self.__processor_type__
