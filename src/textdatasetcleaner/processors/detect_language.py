import os
from typing import Optional
from pathlib import Path

import requests
from fasttext import load_model

from .base import BaseProcessor
from ..helpers import get_line_piece


class DetectLanguageProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, language_code: str, threshold: float = 0.9, delimiter: Optional[str] = None,
                 delimited_position: int = -1, model_url: Optional[str] = None):

        self.language_code = language_code
        self.threshold = threshold
        self.delimiter = delimiter
        self.delimited_position = delimited_position

        # TODO: add project root from config
        self.model_path = 'cache-fasttext.bin'

        if model_url is None:
            model_url = 'https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin'

        self.__download_model(model_url)

        self.ft = load_model(self.model_path)

    def __download_model(self, model_url: str) -> None:
        # TODO: move to helpers
        if os.path.exists(self.model_path):
            return

        response = requests.get(model_url, stream=True)

        if response.status_code != 200:
            # TODO: own exceptions
            raise ValueError(f'Download model {model_url} failed with code {response.status_code}')

        with open(self.model_path, 'wb') as fh:
            for chunk in response.iter_content(chunk_size=16*1024):
                fh.write(chunk)

        # TODO: checksum validation?

    def process_line(self, line: str) -> Optional[str]:
        line_cpy = get_line_piece(line, self.delimiter, self.delimited_position)

        # TODO: `line_cpy = line_cpy.lower()` ?
        result = self.ft.predict(line_cpy, k=1)

        if result[1][0] < self.threshold:
            return None

        lang = result[0][0].replace('__label__', '')

        if lang != self.language_code:
            return None

        return line
