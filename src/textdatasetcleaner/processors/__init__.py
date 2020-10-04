from typing import Dict, Type

from textdatasetcleaner.processors.base import BaseProcessor
from textdatasetcleaner.processors.clean_html import CleanHTMLProcessor
from textdatasetcleaner.processors.clean_symbols import CleanSymbolsProcessor
from textdatasetcleaner.processors.detect_language import DetectLanguageProcessor
from textdatasetcleaner.processors.filter_currency_symbols import FilterCurrencySymbolsProcessor
from textdatasetcleaner.processors.filter_email import FilterEmailProcessor
from textdatasetcleaner.processors.filter_emoji import FilterEmojiProcessor
from textdatasetcleaner.processors.filter_hashtags import FilterHashtagsProcessor
from textdatasetcleaner.processors.filter_numbers import FilterNumbersProcessor
from textdatasetcleaner.processors.filter_phone_number import FilterPhoneNumberProcessor
from textdatasetcleaner.processors.filter_stop_words import FilterStopWordsProcessor
from textdatasetcleaner.processors.filter_url import FilterURLProcessor
from textdatasetcleaner.processors.filter_user_handle import FilterUserHandleProcessor
from textdatasetcleaner.processors.line_convert_case import LineConvertCaseProcessor
from textdatasetcleaner.processors.line_strip import LineStripProcessor
from textdatasetcleaner.processors.normalize_hyphenated_words import NormalizeHyphenatedWordsProcessor
from textdatasetcleaner.processors.normalize_quotation_marks import NormalizeQuotationMarksProcessor
from textdatasetcleaner.processors.normalize_repeating_chars import NormalizeRepeatingCharsProcessor
from textdatasetcleaner.processors.normalize_unicode import NormalizeUnicodeProcessor
from textdatasetcleaner.processors.normalize_whitespace import NormalizeWhitespaceProcessor
from textdatasetcleaner.processors.remove_accents import RemoveAccentsProcessor
from textdatasetcleaner.processors.remove_profanity import RemoveProfanityProcessor
from textdatasetcleaner.processors.shuffle import ShuffleProcessor
from textdatasetcleaner.processors.unique import UniqueProcessor


processors = (
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


processors_types: Dict[str, str] = {}
for proc_t in processors:
    processors_types[proc_t.name] = proc_t.type  # type: ignore

processors_dict: Dict[str, Type[BaseProcessor]] = {}
for proc_d in processors:
    processors_dict[proc_d.name] = proc_d  # type: ignore
