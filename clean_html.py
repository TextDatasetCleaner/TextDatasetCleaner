#!/usr/bin/env python

import os
import re
import shutil
import argparse

import tqdm
from selectolax.parser import HTMLParser

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
        default="datasets/clean_html",
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

    RE_DOUBLE_WS = re.compile(r'[\s+]{2,}')

    with open(args.input_file, encoding='utf-8') as fhr, \
         open(result_filename, 'w', encoding='utf-8') as fhw:
        for i, line in enumerate(tqdm.tqdm(fhr, total=file_lines)):
            if '<' in line and '>' in line:
                tree = HTMLParser(line)
                line = tree.body.text(separator=' ')
                line = RE_DOUBLE_WS.sub(' ', line)

            line = line.strip()
            line = line + "\n"
            fhw.write(line)

    print('Done')
