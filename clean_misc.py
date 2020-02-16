#!/usr/bin/env python

import os
import re
import shutil
import argparse

import tqdm

from putils import (
    file_lines_count
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file",
        help="Input file"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output folder",
        default="datasets/clean_misc",
    )
    parser.add_argument(
        '--remove_old',
        help='Remove old data from output',
        default=True,
        type=lambda x: (str(x).lower() == 'true')
    )

    args = parser.parse_args()

    # create output dir
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    elif args.remove_old:
        shutil.rmtree(args.output)
        os.makedirs(args.output)

    result_filename = os.path.basename(args.input_file)
    result_filename = os.path.join(args.output, result_filename)

    file_lines = file_lines_count(args.input_file)

    RE_SPACE_DOT = re.compile(r'\s+\.\s*')
    RE_MANY_DOT = re.compile(r'\.{4,}')
    RE_MANY_DASH = re.compile(r'[\s\-]{2,}')

    # from textacy
    RE_LINEBREAK = re.compile(r"(\r\n|[\n\v])+")
    RE_NONBREAKING_SPACE = re.compile(r"[^\S\n\v]+", flags=re.UNICODE)

    with open(args.input_file, encoding='utf-8') as fhr, \
         open(result_filename, 'w', encoding='utf-8') as fhw:
        for i, line in enumerate(tqdm.tqdm(fhr, total=file_lines)):
            if '«' in line:
                line = line.replace('«', '"')
            if '»' in line:
                line = line.replace('»', '"')
            if '„' in line:
                line = line.replace('„', '"')
            if '\u0091' in line:
                line = line.replace('\u0091', ' ')
            if '\u0084' in line:
                line = line.replace('\u0084', ' ')
# https://www.htmlsymbols.xyz/punctuation-symbols/quotation-mark
# '\u0022' == '"'
            if '\u02BA' in line:
                line = line.replace('\u02BA', ' ')
            if '\u030B' in line:
                line = line.replace('\u030B', ' ')
            if '\u030E' in line:
                line = line.replace('\u030E', ' ')
            if '\u05F4' in line:
                line = line.replace('\u05F4', ' ')
            if '\u2033' in line:
                line = line.replace('\u2033', ' ')
            if '\u3003' in line:
                line = line.replace('\u3003', ' ')

            if ' .' in line:
                line = RE_SPACE_DOT.sub('.', line)
            if '....' in line:
                line = RE_MANY_DOT.sub('...', line)

            if '—' in line:
                line = line.replace('—', '-')
            if '―' in line:
                line = line.replace('―', '-')
            if '–' in line:
                line = line.replace('–', '-')
            if '\u0096' in line:
                line = line.replace('\u0096', '-')
            if '\u0097' in line:
                line = line.replace('\u0097', '-')
            if '-' in line:
                matches = RE_MANY_DASH.findall(line)
                for match in matches:
                    match = match.strip()
                    if match and len(match) > 1:
                        line  = line.replace(match, '-')

# https://www.htmlsymbols.xyz/punctuation-symbols/space-symbols
# Run in Dev Browser Console:
#
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

            if '\u202C' in line:
                line = line.replace('\u202C', ' ')
            if '\u200E' in line:
                line = line.replace('\u200E', ' ')
            if '\u202A' in line:
                line = line.replace('\u202A', ' ')
            if '\x99' in line:
                line = line.replace('\x99', ' ')

            line = RE_NONBREAKING_SPACE.sub(" ", RE_LINEBREAK.sub(r"\n", line)).strip()

            fhw.write(line + "\n")

    print('Done')
