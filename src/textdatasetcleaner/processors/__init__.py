from typing import Dict

from .base import BaseProcessor
from .clean_html import CleanHTMLProcessor
from .clean_symbols import CleanSymbolsProcessor
from .detect_language import DetectLanguageProcessor
from .filter_currency_symbols import FilterCurrencySymbolsProcessor
from .filter_email import FilterEmailProcessor
from .filter_emoji import FilterEmojiProcessor
from .filter_hashtags import FilterHashtagsProcessor
from .filter_numbers import FilterNumbersProcessor
from .filter_phone_number import FilterPhoneNumberProcessor
from .filter_stop_words import FilterStopWordsProcessor
from .filter_url import FilterURLProcessor
from .filter_user_handle import FilterUserHandleProcessor
from .line_convert_case import LineConvertCaseProcessor
from .line_strip import LineStripProcessor
from .normalize_hyphenated_words import NormalizeHyphenatedWordsProcessor
from .normalize_quotation_marks import NormalizeQuotationMarksProcessor
from .normalize_repeating_chars import NormalizeRepeatingCharsProcessor
from .normalize_unicode import NormalizeUnicodeProcessor
from .normalize_whitespace import NormalizeWhitespaceProcessor
from .remove_accents import RemoveAccentsProcessor
from .remove_profanity import RemoveProfanityProcessor
from .shuffle import ShuffleProcessor
from .unique import UniqueProcessor


__all__ = (
    CleanHTMLProcessor,
    CleanSymbolsProcessor,
    DetectLanguageProcessor,
    FilterCurrencySymbolsProcessor,
    FilterEmailProcessor,
    FilterEmojiProcessor,
    FilterHashtagsProcessor,
    FilterNumbersProcessor,
    FilterPhoneNumberProcessor,
    FilterStopWordsProcessor,
    FilterURLProcessor,
    FilterUserHandleProcessor,
    LineConvertCaseProcessor,
    LineStripProcessor,
    NormalizeHyphenatedWordsProcessor,
    NormalizeQuotationMarksProcessor,
    NormalizeRepeatingCharsProcessor,
    NormalizeUnicodeProcessor,
    NormalizeWhitespaceProcessor,
    RemoveAccentsProcessor,
    RemoveProfanityProcessor,
    ShuffleProcessor,
    UniqueProcessor,
)


processors_types = {p.name: p.type for p in __all__}  # type: Dict[str: str]
processors_dict = {p.name: p for p in __all__}  # type: Dict[str: BaseProcessor]
