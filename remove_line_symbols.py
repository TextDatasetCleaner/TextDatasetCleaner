#!/usr/bin/env python

import os
import pickle
import shutil
import argparse
from pprint import pprint

import tqdm

from putils import file_lines_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file",
        help="Input file"
    )
    parser.add_argument(
        "-c",
        "--count",
        help="Min count of repeats for remove this symbols",
        default=100
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output folder",
        default="datasets/remove_line_symbols",
    )
    parser.add_argument(
        '--remove_old',
        help='Remove old data from output',
        default=True,
        type=lambda x: (str(x).lower() == 'true')
    )

    args = parser.parse_args()

    count = input('Write count for remove line with this symbols: ')
    if not count:
        count = args.count
        print('use default count: ', count)
    count = int(count)

    # create output dir
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    elif args.remove_old:
        shutil.rmtree(args.output)
        os.makedirs(args.output)

    result_filename = os.path.basename(args.input_file)
    result_filename = os.path.join(args.output, result_filename)

    symbols = {}
    file_lines = file_lines_count(args.input_file)

    with open(args.input_file + ".pickled", 'rb') as fhr:
        symbols = pickle.load(fhr)

    symbs = list()
    for data in symbols:
        if data[1] <= count:
            symbs.append(data[0])

    with open(args.input_file, encoding='utf-8') as fhr, \
         open(result_filename, 'w', encoding='utf-8') as fhw:
        for i, line in enumerate(tqdm.tqdm(fhr, total=file_lines)):
            need_remove = False
            for char in symbs:
                if char in line:
                    need_remove = True
                    break
            if not need_remove:
                fhw.write(line.strip() + "\n")

    print('Done')
