#!/bin/bash

ROOT=`pwd`
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

DATASET_NAME="$1"


if [ -f "${ROOT}/requirements.txt" ]
then
    echo -e "${GREEN}Install requirements:${NC}"

    # TODO: fix incompatibility warning in tensorflow/tensorflow:1.15.0-gpu-py3 docker container
    pip uninstall -y numpy

    pip install -r ${ROOT}/requirements.txt
    if [ $? -ne 0 ]
    then
        echo -e "${RED}FAILED${NC}"
        exit 1
    fi
    rm ${ROOT}/requirements.txt
fi


if [ ! -f "datasets/${DATASET_NAME}.txt" ]
then
    echo -e "${DATASET_NAME} not found in datasets folder"
    exit 1
fi

echo -e "${GREEN}Fix soft ulimit:${NC}"
# for `shuf` command below
ulimit -S -n 10000
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


echo -e "${GREEN}Clean HTML:${NC}"
python clean_html.py datasets/${DATASET_NAME}.txt
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


echo -e "${GREEN}Check lid.176.bin:${NC}"
mkdir -p ${ROOT}/tmp
if [ ! -f "${ROOT}/tmp/lid.176.bin" ]
then
    echo -e "${GREEN}Download lid.176.bin:${NC}"
    wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin ${ROOT}/tmp/lid.176.bin
fi


echo -e "${GREEN}Detect language:${NC}"
python detect_lang.py --model=${ROOT}/tmp/lid.176.bin datasets/clean_html/${DATASET_NAME}.txt
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


echo -e "${GREEN}Filter textacy:${NC}"
python filter_textacy.py datasets/detect_lang/${DATASET_NAME}_en.txt
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


echo -e "${GREEN}Filter profanity:${NC}"
python filter_profanity.py datasets/filter_textacy/${DATASET_NAME}_en.txt
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


echo -e "${GREEN}Clean misc:${NC}"
python clean_misc.py datasets/filter_profanity/${DATASET_NAME}_en.txt
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


echo -e "${GREEN}Remove duplicates:${NC}"
# fastest method
sort datasets/clean_misc/${DATASET_NAME}_en.txt | uniq > datasets/clean_misc/${DATASET_NAME}_uniq.txt
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


echo -e "${GREEN}Shuffle:${NC}"
shuf -o datasets/${DATASET_NAME}_shuffled.txt < datasets/clean_misc/${DATASET_NAME}_uniq.txt
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


echo -e "${GREEN}Calc symbols:${NC}"
python calc_symbols.py datasets/${DATASET_NAME}_shuffled.txt > datasets/${DATASET_NAME}_symbols.txt


echo -e "${GREEN}Show symbols map:${NC}"
less datasets/${DATASET_NAME}_symbols.txt


echo -e "${GREEN}Remove lines with bad symbols:${NC}"
python remove_line_symbols.py datasets/${DATASET_NAME}_shuffled.txt
if [ $? -ne 0 ]
then
    echo -e "${RED}FAILED${NC}"
    exit 1
fi


mv datasets/remove_line_symbols/${DATASET_NAME}_shuffled.txt datasets/${DATASET_NAME}_result.txt
echo -e "${GREEN}Result file: datasets/${DATASET_NAME}_result.txt${NC}"
