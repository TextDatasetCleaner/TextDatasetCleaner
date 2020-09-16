from .detect_language import DetectLanguageProcessor
from .line_strip import LineStripProcessor
from .shuffle import ShuffleProcessor
from .unique import UniqueProcessor


processors_dict = {
    DetectLanguageProcessor.name: DetectLanguageProcessor,
    LineStripProcessor.name: LineStripProcessor,
    ShuffleProcessor.name: ShuffleProcessor,
    UniqueProcessor.name: UniqueProcessor,
}
