from typing import Dict

from .base import BaseProcessor
from .clean_html import CleanHTMLProcessor
from .clean_symbols import CleanSymbolsProcessor
from .detect_language import DetectLanguageProcessor
from .filter_profanity import FilterProfanityProcessor
from .filter_textacy import FilterTextacyProcessor
from .line_convert_case import LineConvertCaseProcessor
from .line_strip import LineStripProcessor
from .shuffle import ShuffleProcessor
from .unique import UniqueProcessor


__all__ = (
    CleanHTMLProcessor,
    CleanSymbolsProcessor,
    DetectLanguageProcessor,
    FilterProfanityProcessor,
    FilterTextacyProcessor,
    LineConvertCaseProcessor,
    LineStripProcessor,
    ShuffleProcessor,
    UniqueProcessor,
)


processors_types = {p.name: p.type for p in __all__}  # type: Dict[str: str]
processors_dict = {p.name: p for p in __all__}  # type: Dict[str: BaseProcessor]
