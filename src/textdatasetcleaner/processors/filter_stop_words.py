import json
import re
from pathlib import Path
from typing import Optional

from .base import BaseProcessor
from ..helpers import download_file, get_temp_file_path
from ..exceptions import TDSValueError


class FilterStopWordsProcessor(BaseProcessor):

    __processor_name__ = Path(__file__).resolve().stem
    __processor_type__ = 'line'

    def __init__(self, language_code: str, mode: str, replace_with: str = ' '):
        allowed_language = [
            # https://github.com/6/stopwords-json/tree/master/dist
            # Run in Dev Browser Console:
            # var l = '';
            # $x("//a[starts-with(@href, '/6/stopwords-json/blob/master/dist/')]/@href").forEach(function(el) {
            #   var code = el.textContent.replace('/6/stopwords-json/blob/master/dist/', '').replace('.json', '');
            #   languages = languages + "'" + code + "',\n";
            # });
            # console.log(languages);
            'af',
            'ar',
            'bg',
            'bn',
            'br',
            'ca',
            'cs',
            'da',
            'de',
            'el',
            'en',
            'eo',
            'es',
            'et',
            'eu',
            'fa',
            'fi',
            'fr',
            'ga',
            'gl',
            'ha',
            'he',
            'hi',
            'hr',
            'hu',
            'hy',
            'id',
            'it',
            'ja',
            'ko',
            'la',
            'lv',
            'mr',
            'nl',
            'no',
            'pl',
            'pt',
            'ro',
            'ru',
            'sk',
            'sl',
            'so',
            'st',
            'sv',
            'sw',
            'th',
            'tr',
            'yo',
            'zh',
            'zu',
        ]
        if language_code not in allowed_language:
            raise TDSValueError(f'Wrong language for {self.name} processor: {language_code}, allowed only: {allowed_language}')
        self.language_code = language_code

        url = f'https://raw.githubusercontent.com/6/stopwords-json/master/dist/{self.language_code}.json'
        temp_file = get_temp_file_path()

        # FIXME: write & read? Better download to variable
        download_file(url, temp_file)
        with open(temp_file, encoding='utf-8') as fd:
            stop_words = fd.read()

        stop_words = json.loads(stop_words)
        stop_words = set(w.replace('|', '') for w in stop_words)
        stop_words = '|'.join(stop_words)
        self.stop_words_re = re.compile(rf'\b({stop_words})\b', flags=re.UNICODE | re.IGNORECASE)

        allowed = ['remove_line', 'replace']
        if mode not in allowed:
            raise TDSValueError(f'Wrong mode for {self.name} processor: {mode}, allowed only: {allowed}')

        self.mode = mode
        self.replace_with = replace_with

    def process_line(self, line: str) -> Optional[str]:
        if self.mode == 'remove_line':
            if self.stop_words_re.search(line):
                return None

        elif self.mode == 'replace':
            # TODO: bench 'sub' vs 'search + sub'
            line = self.stop_words_re.sub(self.replace_with, line)

        return line
