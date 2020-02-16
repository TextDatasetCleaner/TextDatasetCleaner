#!/usr/bin/env python

import os
import shutil
import string
import argparse

import tqdm
from textacy.preprocessing import (
    normalize_hyphenated_words,
    normalize_quotation_marks,
    normalize_unicode,
    normalize_whitespace,
    remove_accents,
    replace_emails,
    normalize_repeating_chars
)
from textacy.preprocessing.resources import (
    RE_EMAIL,
    RE_SHORT_URL,
    RE_URL
)

from putils import (
    file_lines_count,
    write_wrong
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
        default="datasets/filter_textacy",
    )
    parser.add_argument(
        '--remove_old',
        help='Remove old data from output',
        default=True,
        type=lambda x: (str(x).lower() == 'true')
    )
    parser.add_argument(
        '--write_bad',
        help='Write bad lines to file',
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

    fh_bad = None
    if args.write_bad:
        fh_bad = open(result_filename + '.bad', 'w', encoding='utf-8')

    punctuation_map = string.punctuation.replace('.', '') # prevent remove '...'
    punctuation_map = string.punctuation.replace('\\', '') # FIXME: error in slash escaping inside of normalize_repeating_chars

    file_lines = file_lines_count(args.input_file)
    with open(args.input_file, encoding='utf-8') as fhr, \
         open(result_filename, 'w', encoding='utf-8') as fhw:
        for i, line in enumerate(tqdm.tqdm(fhr, total=file_lines)):
            line = line.strip()

            # TODO: maybe remove urls / emails, not skip?
            # not fix bad lines
            if RE_SHORT_URL.search(line):
                write_wrong(fh_bad, line + "\n")
                continue
            if RE_URL.search(line):
                write_wrong(fh_bad, line + "\n")
                continue
            if RE_EMAIL.search(line):
                write_wrong(fh_bad, line + "\n")
                continue

            # fixes and normalization
            line = remove_accents(line)
            line = normalize_hyphenated_words(line)
            line = normalize_quotation_marks(line)
            line = normalize_unicode(line, form='NFKC')

            # repeating symbols
            for punct in punctuation_map:
                if punct in line:
                    line = normalize_repeating_chars(line, chars=punct, maxn=1)
            if '....' in line:
                line = normalize_repeating_chars(line, chars='.', maxn=3)

            # need be last
            line = normalize_whitespace(line)

            # if line not empty - write line to output
            if line:
                fhw.write(line + "\n")

    if fh_bad:
        fh_bad.close()

    print('Done')