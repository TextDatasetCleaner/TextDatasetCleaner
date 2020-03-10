#!/usr/bin/env python

import pickle
import argparse
from pprint import pprint
from itertools import islice
from string import punctuation
from collections import Counter

import tqdm
from nltk.tokenize import ToktokTokenizer

from putils import file_lines_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--delimiter",
        help="Delimiter (get last value)",
        default=":|:",
    )
    parser.add_argument(
        "-m",
        "--max",
        help="Max most common items",
        default=15,
        type=int
    )
    parser.add_argument(
        "input_file",
        help="Input file"
    )

    args = parser.parse_args()

    freq = {i:0 for i in range(args.max)}

    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
    punct_trans = str.maketrans('', '', punctuation)

    file_lines = file_lines_count(args.input_file)
    with open(args.input_file, encoding='utf-8') as fhr:
        for i, line in enumerate(tqdm.tqdm(fhr, total=file_lines)):
            if line.find(args.delimiter) != -1:
                line = line.split(args.delimiter)[-1]

            # https://stackoverflow.com/questions/41912083/nltk-tokenize-faster-way
            toktok = ToktokTokenizer()
            tokens = [x for x in toktok.tokenize(line.lower().translate(punct_trans))]

            counter = Counter()
            total_grams = 0

            # https://stackoverflow.com/a/22004007/1574977
            for gram in zip(tokens, islice(tokens, 1, None)):  # faster than nltk.bigrams
                total_grams += 1
                counter[gram] += 1

            i = 0
            for item in counter.most_common(args.max):
                freq[i] += item[1] / total_grams
                i += 1

    for i in range(args.max):
        freq[i] = freq[i] / file_lines

    with open(args.input_file + ".pickled", 'wb') as fhr:
        fhr.write(pickle.dumps(freq))

    # print to stdout = save to file with pipe
    pprint(freq)
