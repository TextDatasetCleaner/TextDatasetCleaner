from typing import Dict

from .base import BaseProcessor
from .clean_html import CleanHTMLProcessor
from .detect_language import DetectLanguageProcessor
from .filter_textacy import FilterTextacyProcessor
from .line_strip import LineStripProcessor
from .shuffle import ShuffleProcessor
from .unique import UniqueProcessor


__all__ = (
    CleanHTMLProcessor,
    DetectLanguageProcessor,
    FilterTextacyProcessor,
    LineStripProcessor,
    ShuffleProcessor,
    UniqueProcessor,
)


processors_types = {p.name: p.type for p in __all__}  # type: Dict[str: str]
processors_dict = {p.name: p for p in __all__}  # type: Dict[str: BaseProcessor]
