from pytest import mark

from textdatasetcleaner.processors import CleanSymbolsProcessor
from textdatasetcleaner.processors.clean_symbols import (
    DASHES,
    DOUBLE_QUOTES,
    EXCLAMATIONS,
    NON_PRINTABLE,
    QUESTIONS,
    SINGLE_QUOTES,
    SPACES,
)


class TestCleanSymbols:
    def setup(self):
        self.processor = CleanSymbolsProcessor()
        self.line = 'Some text with {symbol} symbol'

    @mark.parametrize('symbol', DOUBLE_QUOTES)
    def test__double_quote(self, symbol):
        assert self.processor.process_line(self.line.format(symbol=symbol)) == 'Some text with " symbol'

    @mark.parametrize('symbol', SINGLE_QUOTES)
    def test__single_quote(self, symbol):
        assert self.processor.process_line(self.line.format(symbol=symbol)) == "Some text with ' symbol"

    @mark.parametrize('symbol', DASHES)
    def test__dash(self, symbol):
        assert self.processor.process_line(self.line.format(symbol=symbol)) == 'Some text with - symbol'

    @mark.parametrize('symbol', SPACES)
    def test__space(self, symbol):
        assert self.processor.process_line(self.line.format(symbol=symbol)) == 'Some text with   symbol'

    @mark.parametrize('symbol', NON_PRINTABLE)
    def test__non_printable(self, symbol):
        assert self.processor.process_line(self.line.format(symbol=symbol)) == 'Some text with   symbol'

    @mark.parametrize('symbol', EXCLAMATIONS)
    def test__exclamation(self, symbol):
        assert self.processor.process_line(self.line.format(symbol=symbol)) == 'Some text with ! symbol'

    @mark.parametrize('symbol', QUESTIONS)
    def test__question(self, symbol):
        assert self.processor.process_line(self.line.format(symbol=symbol)) == 'Some text with ? symbol'

    def test__duplicate_dashes(self):
        should_be = 'Some - text'

        assert self.processor.process_line('Some - text') == should_be
        assert self.processor.process_line('Some -- text') == should_be
        assert self.processor.process_line('Some --- text') == should_be

    def test__dot_at_end(self):
        should_be = 'Some random. Text two'

        assert self.processor.process_line('Some random . Text two') == should_be
        assert self.processor.process_line('Some random .  Text two') == should_be
        assert self.processor.process_line('Some random  . Text two') == should_be
        assert self.processor.process_line('Some random  .  Text two') == should_be
