#!/usr/bin/env python

import os
import shutil
import argparse

import tqdm
from profanity_check import predict_prob

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
        default="datasets/filter_profanity",
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
    parser.add_argument(
        "-t",
        "--threshold",
        help="Min threshold",
        default=0.90
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

    file_lines = file_lines_count(args.input_file)
    with open(args.input_file, encoding='utf-8') as fhr, \
         open(result_filename, 'w', encoding='utf-8') as fhw:
        for i, line in enumerate(tqdm.tqdm(fhr, total=file_lines)):
            # detect profinity line
            if predict_prob([line])[0] > args.threshold:
                write_wrong(fh_bad, line)
                continue

            line = line.strip()
            line = line + "\n"
            fhw.write(line)

    if fh_bad:
        fh_bad.close()

    print('Done')
