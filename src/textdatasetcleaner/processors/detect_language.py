import os
from pathlib import Path
from typing import Optional

from fasttext import load_model

from .base import BaseProcessor
from ..helpers import download_file, get_line_piece, get_temp_file_path


class DetectLanguageProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, language_code: str, threshold: float = 0.9, model_path: Optional[str] = None,
                 model_url: Optional[str] = None, delimiter: Optional[str] = None, delimited_position: int = -1):

        self.language_code = language_code
        self.threshold = threshold

        self.delimiter = delimiter
        self.delimited_position = delimited_position

        self.model_path = model_path
        self.model_url = model_url

        if not self.model_url:
            # https://fasttext.cc/docs/en/language-identification.html
            self.model_url = 'https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin'

        if not self.model_path:
            # TODO: log model_path
            self.model_path = get_temp_file_path()

        if not os.path.exists(self.model_path):
            download_file(self.model_url, self.model_path)

        self.ft = load_model(self.model_path)

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
