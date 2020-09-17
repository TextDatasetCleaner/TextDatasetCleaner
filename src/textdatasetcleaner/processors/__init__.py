from .detect_language import DetectLanguageProcessor
from .line_strip import LineStripProcessor
from .shuffle import ShuffleProcessor
from .unique import UniqueProcessor


__all__ = (
    DetectLanguageProcessor,
    LineStripProcessor,
    ShuffleProcessor,
    UniqueProcessor,
)


processors_types = {p.name: p.type for p in __all__}
processors_dict = {p.name: p for p in __all__}
