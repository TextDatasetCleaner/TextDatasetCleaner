from abc import ABC
from typing import Any, Optional

from textdatasetcleaner.exceptions import TDCNotImplemented
from textdatasetcleaner.helpers import ClassProperty


class BaseProcessor(ABC):

    __processor_name__: str = ''
    __processor_type__: str = ''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Implement in child class."""

    def process_line(self, line: str) -> Optional[str]:
        raise TDCNotImplemented()

    def process_file(self, input_file: str, output_file: str) -> bool:
        raise TDCNotImplemented()

    @ClassProperty
    def name(self) -> str:
        if not self.__processor_name__:
            raise TDCNotImplemented('Processor name not overloaded!')
        return self.__processor_name__

    @ClassProperty
    def type(self) -> str:
        if not self.__processor_type__:
            raise TDCNotImplemented('Processor type not overloaded!')
        return self.__processor_type__
