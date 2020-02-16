#!/usr/bin/env python

# run:
# python detect_lang.py titles.txt
# or see help:
# python detect_lang.py -h

import os
import shutil
import operator
import argparse


import tqdm
from fasttext import load_model  # https://github.com/facebookresearch/fastText/tree/master/python

from putils import file_lines_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Predict titles from file and move this to lang subdirs"
        )
    )
    parser.add_argument(
        "input_file",
        help="Input file for prediction"
    )
    parser.add_argument(
        "--model",
        help="Model to use",
        default='tmp/lid.176.bin'
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        help="Delimiter (get last value)",
        default=":|:",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output folder",
        default="datasets/detect_lang",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        help="Max threshold for set lang to unknown",
        default=0.90
    )
    parser.add_argument(
        '--save_langs',
        help='Save only languages from this parameter',
        default='en'
    )
    parser.add_argument(
        '--remove_old',
        help='Remove old data from output',
        default=True,
        type=lambda x: (str(x).lower() == 'true')
    )
    args = parser.parse_args()

    # load model from arg
    f = load_model(args.model)

    # create output dir
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    elif args.remove_old:
        shutil.rmtree(args.output)
        os.makedirs(args.output)

    # result filehandlers
    result = dict()

    # result filename
    result_filename = os.path.splitext(os.path.basename(args.input_file))
    result_filename = result_filename[0] + '_{0}' + result_filename[1]
    result_filename = os.path.join(args.output, result_filename)

    save_langs = args.save_langs.split(',')

    file_lines = file_lines_count(args.input_file)

    # get prediction for every line
    with open(args.input_file, encoding='utf-8') as fhr:
        for i, line in enumerate(tqdm.tqdm(fhr, total=file_lines)):
            line = line.strip()

            text = line
            delim_pos = line.find(args.delimiter)
            if delim_pos != -1:
                text = line.split(args.delimiter)[-1]

            text = text.lower()
            predict_result = f.predict(text)


            if predict_result[1][0] < args.threshold:
                lang = 'unknown'
            else:
                lang = predict_result[0][0].replace('__label__', '')

            if lang in save_langs:
                if lang not in result:
                    lang_output_path = result_filename.format(lang)
                    result[lang] = open(lang_output_path, 'w', encoding='utf-8')

                result[lang].write(line + "\n")

    # close open files
    for langkey in result:
        result[langkey].close()

    print('Done all')
