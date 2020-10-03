import re
from pathlib import Path
from typing import Optional

from .base import BaseProcessor


DOUBLE_QUOTES = [
    '«',
    '»',
    '„',
    # https://www.htmlsymbols.xyz/punctuation-symbols/quotation-mark
    # '\u0022' == '"'
    '\u02BA',  # ʺ
    '\u030B',  # ̋
    '\u030E',  # ̎
    '\u05F4',  # ״
    '\u2033',  # ″
    '\u3003',  # 〃
    # https://github.com/jfilter/clean-text/blob/master/cleantext/constants.py#L97-L114
    '‹',
    '›',
    "“",
    "‟",
    "”",
    "❝",
    "❞",
    "❮",
    "❯",
    "〝",
    "〞",
    "〟",
    "＂",
]
SINGLE_QUOTES = [
    # https://github.com/jfilter/clean-text/blob/master/cleantext/constants.py#L115
    "‘",
    "‛",
    "’",
    "❛",
    "❜",
    "`",
    "´",
]
DASHES = [
    '—',  # em dash
    '–',  # en dash
    '―',  # horizontal bar
]
SPACES = [
    # https://www.htmlsymbols.xyz/punctuation-symbols/space-symbols
    # Run in Dev Browser Console:
    # var symbols = '';
    # $x('//a[contains(@class, "content-item")]/div[@class="two-in-one"][3]/span').forEach(function(el) {
    #   symbols = symbols + "    '\\u" + el.textContent.replace('\\', '') + "',\n";
    # });
    # console.log(symbols);
    '\u00A0',
    '\u0180',
    '\u2000',
    '\u2001',
    '\u2002',
    '\u2003',
    '\u2004',
    '\u2005',
    '\u2007',
    '\u2008',
    '\u2009',
    '\u200A',
    '\u200B',
    '\u2060',
    '\u2334',
    '\u2422',
    '\u2423',
    '\u2E00',
    '\u3000',
    '\uFEFF',

    # spaces 2
    '\u0084',
    '\u0091',
    '\u0096',
    '\u0097',

    # spaces 3
    '\u202C',
    '\u200E',
    '\u202A',
    '\x99',
]
NON_PRINTABLE = [
    # https://github.com/pudo/normality/blob/master/normality/cleaning.py#L10
    # for s in range(ord('\x00'), ord('\x08')): print(f"{chr(s)!r},   #  chr({s})")
    '\x00',  # chr(0)
    '\x01',  # chr(1)
    '\x02',  # chr(2)
    '\x03',  # chr(3)
    '\x04',  # chr(4)
    '\x05',  # chr(5)
    '\x06',  # chr(6)
    '\x07',  # chr(7)
    '\x0b',  # chr(11)
    '\x0e',  # chr(14)
    '\x0f',  # chr(15)
    '\x10',  # chr(16)
    '\x11',  # chr(17)
    '\x12',  # chr(18)
    '\x13',  # chr(19)
    '\x14',  # chr(20)
    '\x15',  # chr(21)
    '\x16',  # chr(22)
    '\x17',  # chr(23)
    '\x18',  # chr(24)
    '\x19',  # chr(25)
    '\x1a',  # chr(26)
    '\x1b',  # chr(27)
    '\x1c',  # chr(28)
    '\x1d',  # chr(29)
    '\x1e',  # chr(30)
    '\x7f',  # chr(127)
    '\x80',  # chr(128)
    '\x81',  # chr(129)
    '\x82',  # chr(130)
    '\x83',  # chr(131)
    '\x84',  # chr(132)
    '\x85',  # chr(133)
    '\x86',  # chr(134)
    '\x87',  # chr(135)
    '\x88',  # chr(136)
    '\x89',  # chr(137)
    '\x8a',  # chr(138)
    '\x8b',  # chr(139)
    '\x8c',  # chr(140)
    '\x8d',  # chr(141)
    '\x8e',  # chr(142)
    '\x8f',  # chr(143)
    '\x90',  # chr(144)
    '\x91',  # chr(145)
    '\x92',  # chr(146)
    '\x93',  # chr(147)
    '\x94',  # chr(148)
    '\x95',  # chr(149)
    '\x96',  # chr(150)
    '\x97',  # chr(151)
    '\x98',  # chr(152)
    '\x99',  # chr(153)
    '\x9a',  # chr(154)
    '\x9b',  # chr(155)
    '\x9c',  # chr(156)
    '\x9d',  # chr(157)
    '\x9e',  # chr(158)
]
EXCLAMATIONS = [
    # HTTPS://WWW.HTMLSYMBOLS.XYZ/PUNCTUATION-SYMBOLS/EXCLAMATION-MARK
    # '\U0021 == '!'
    '\u00A1',  # ¡
    '\u01C3',  # ǃ
    '\u203C',  # ‼
    '\u2762',  # ❢
]
QUESTIONS = [
    # https://www.htmlsymbols.xyz/search?q=question
    '\u203D',  # ‽
    '\u00BF',  # ¿
    '\uFF1F',  # ？
]

RE_SPACE_DOT = re.compile(r'\s+\.\s*')
RE_MANY_DASH = re.compile(r'[\s\-]{2,}')


class CleanSymbolsProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        for symbol in DOUBLE_QUOTES:
            line = line.replace(symbol, '"')

        for symbol in SINGLE_QUOTES:
            line = line.replace(symbol, "'")

        for symbol in DASHES:
            line = line.replace(symbol, '-')

        for symbol in SPACES:
            line = line.replace(symbol, ' ')

        for symbol in NON_PRINTABLE:
            line = line.replace(symbol, '')

        for symbol in EXCLAMATIONS:
            line = line.replace(symbol, ' ')

        for symbol in QUESTIONS:
            line = line.replace(symbol, ' ')

        # duplicate dashes
        if '-' in line:
            matches = RE_MANY_DASH.findall(line)
            for match in matches:
                match = match.strip()
                if match and len(match) > 1:
                    line = line.replace(match, '-')

        # fix 'abc    .     cba'
        if ' .' in line:
            line = RE_SPACE_DOT.sub('. ', line)
            line = line.strip()

        return line
