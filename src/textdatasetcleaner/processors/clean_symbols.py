import re
from pathlib import Path
from typing import Optional

from .base import BaseProcessor


RE_SPACE_DOT = re.compile(r'\s+\.\s*')
RE_MANY_DASH = re.compile(r'[\s\-]{2,}')


class CleanSymbolsProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def process_line(self, line: str) -> Optional[str]:
        double_quotes = [
            '«',
            '»',
            '„',
            # https://www.htmlsymbols.xyz/punctuation-symbols/quotation-mark
            # '\u0022' == '"'
            '\u02BA',   # ʺ
            '\u030B',   #  ̋
            '\u030E',   #  ̎
            '\u05F4',   # ״
            '\u2033',   # ″
            '\u3003',   # 〃
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
        for symbol in double_quotes:
            line = line.replace(symbol, '"')

        single_quotes = [
            # https://github.com/jfilter/clean-text/blob/master/cleantext/constants.py#L115
            "‘",
            "‛",
            "’",
            "❛",
            "❜",
            "`",
            "´",
        ]
        for symbol in single_quotes:
            line = line.replace(symbol, "'")

        dashes = [
            '—',    # em dash
            '–',    # en dash
            '―',    # horizontal bar
        ]
        for symbol in dashes:
            line = line.replace(symbol, '-')

        # duplicate dashes
        if '-' in line:
            matches = RE_MANY_DASH.findall(line)
            for match in matches:
                match = match.strip()
                if match and len(match) > 1:
                    line = line.replace(match, '-')

        spaces = [
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
        for symbol in spaces:
            line = line.replace(symbol, ' ')

        exclamations = [
            # https://www.htmlsymbols.xyz/punctuation-symbols/exclamation-mark
            # '\u0021 == '!'
            '\u00A1',   # ¡
            '\u01C3',   # ǃ
            '\u203C',   # ‼
            '\u2762',   # ❢
        ]
        for symbol in exclamations:
            line = line.replace(symbol, ' ')

        questions = [
            # https://www.htmlsymbols.xyz/search?q=question
            '\u203D',   # ‽
            '\u00BF',   # ¿
            '\uFF1F',   # ？
        ]
        for symbol in questions:
            line = line.replace(symbol, ' ')

        # fix 'abc    .     cba'
        if ' .' in line:
            line = RE_SPACE_DOT.sub('. ', line)
            line = line.strip()

        return line
