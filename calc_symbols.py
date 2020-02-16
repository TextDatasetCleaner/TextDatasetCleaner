#!/usr/bin/env python

import pickle
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

    args = parser.parse_args()

    symbols = {}

    file_lines = file_lines_count(args.input_file)

    with open(args.input_file, encoding='utf-8') as fhr:
        for i, line in enumerate(tqdm.tqdm(fhr, total=file_lines)):
            for char in set(line):
                if char in symbols:
                    symbols[char] += 1
                else:
                    symbols[char] = 1

    symbols = sorted(symbols.items(), key=lambda kv: kv[1], reverse=True)
    pickled_symbols = pickle.dumps(symbols)
    with open(args.input_file + ".pickled", 'wb') as fhr:
        fhr.write(pickled_symbols)

    # print to stdout = save to file with pipe
    pprint(symbols)
