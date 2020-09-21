import re
from pathlib import Path
from typing import Optional

from .base import BaseProcessor


RE_SPACE_DOT = re.compile(r'\s+\.\s*')
RE_MANY_DASH = re.compile(r'[\s\-]{2,}')

# from textacy
RE_LINEBREAK = re.compile(r'(\r\n|[\n\v])+')
RE_NONBREAKING_SPACE = re.compile(r'[^\S\n\v]+', flags=re.UNICODE)


class CleanSymbolsProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, or_condition: bool = False):
        self.or_condition = or_condition

    def process_line(self, line: str) -> Optional[str]:
        # quotation mark
        # https://www.htmlsymbols.xyz/punctuation-symbols/quotation-mark
        # '\u0022' == '"'
        if '«' in line:
            line = line.replace('«', '"')
        if '»' in line:
            line = line.replace('»', '"')
        if '„' in line:
            line = line.replace('„', '"')
        if '\u02BA' in line:    # ʺ
            line = line.replace('\u02BA', ' ')
        if '\u030B' in line:    #  ̋
            line = line.replace('\u030B', ' ')
        if '\u030E' in line:    #  ̎
            line = line.replace('\u030E', ' ')
        if '\u05F4' in line:    # ״
            line = line.replace('\u05F4', ' ')
        if '\u2033' in line:    # ″
            line = line.replace('\u2033', ' ')
        if '\u3003' in line:    # 〃
            line = line.replace('\u3003', ' ')

        if ' .' in line:
            line = RE_SPACE_DOT.sub('. ', line)

        # dash
        if '—' in line:     # em dash
            line = line.replace('—', '-')
        if '–' in line:     # en dash
            line = line.replace('–', '-')
        if '―' in line:     # horizontal bar
            line = line.replace('―', '-')
        if '-' in line:     # dash
            matches = RE_MANY_DASH.findall(line)
            for match in matches:
                match = match.strip()
                if match and len(match) > 1:
                    line = line.replace(match, '-')

        # spaces
        # https://www.htmlsymbols.xyz/punctuation-symbols/space-symbols
        # Run in Dev Browser Console:
        # $x('//a[contains(@class, "content-item")]/div[@class="two-in-one"][3]/span').forEach(function(el) {
        #   var symb = el.textContent.replace('\\', '');
        #   console.log("if '\\u" + symb + "' in line:\n    line = line.replace('\\u" + symb + "', ' ')");
        # });
        if '\u00A0' in line:
            line = line.replace('\u00A0', ' ')
        if '\u0180' in line:
            line = line.replace('\u0180', ' ')
        if '\u2000' in line:
            line = line.replace('\u2000', ' ')
        if '\u2001' in line:
            line = line.replace('\u2001', ' ')
        if '\u2002' in line:
            line = line.replace('\u2002', ' ')
        if '\u2003' in line:
            line = line.replace('\u2003', ' ')
        if '\u2004' in line:
            line = line.replace('\u2004', ' ')
        if '\u2005' in line:
            line = line.replace('\u2005', ' ')
        if '\u2007' in line:
            line = line.replace('\u2007', ' ')
        if '\u2008' in line:
            line = line.replace('\u2008', ' ')
        if '\u2009' in line:
            line = line.replace('\u2009', ' ')
        if '\u200A' in line:
            line = line.replace('\u200A', ' ')
        if '\u200B' in line:
            line = line.replace('\u200B', ' ')
        if '\u2060' in line:
            line = line.replace('\u2060', ' ')
        if '\u2334' in line:
            line = line.replace('\u2334', ' ')
        if '\u2422' in line:
            line = line.replace('\u2422', ' ')
        if '\u2423' in line:
            line = line.replace('\u2423', ' ')
        if '\u2E00' in line:
            line = line.replace('\u2E00', ' ')
        if '\u3000' in line:
            line = line.replace('\u3000', ' ')
        if '\uFEFF' in line:
            line = line.replace('\uFEFF', ' ')

        # spaces 2
        if '\u0084' in line:
            line = line.replace('\u0084', ' ')
        if '\u0091' in line:
            line = line.replace('\u0091', ' ')
        if '\u0096' in line:
            line = line.replace('\u0096', ' ')
        if '\u0097' in line:
            line = line.replace('\u0097', ' ')

        # spaces 3
        if '\u202C' in line:
            line = line.replace('\u202C', ' ')
        if '\u200E' in line:
            line = line.replace('\u200E', ' ')
        if '\u202A' in line:
            line = line.replace('\u202A', ' ')
        if '\x99' in line:
            line = line.replace('\x99', ' ')

        line = RE_NONBREAKING_SPACE.sub(' ', RE_LINEBREAK.sub(r'\n', line)).strip()

        return line
