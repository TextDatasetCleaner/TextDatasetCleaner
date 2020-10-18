from unittest.mock import mock_open, patch

from textdatasetcleaner.helpers import get_line_piece, load_config


class TestLoadConfig:
    def test__empty(self):
        path = '/path/to/config'
        read_data = ''

        with patch('builtins.open', mock_open(read_data=read_data)) as mock_file:
            result = load_config(path)
            mock_file.assert_called_with(path)

        assert result is None

    def test__ok(self):
        path = '/path/to/config'
        read_data = """
PRE_PROCESSING:
  - unique
PROCESSING:
  - detect_language:
      language_code: ru
      delimiter: '~'
      delimited_position: -1
      model_path: '/path/fasttext-lid.176.bin'
  - remove_accents
POST_PROCESSING:
  - shuffle

CACHE_DIR: '/cache/tdc'
        """

        should_be = {
            'PRE_PROCESSING': [
                'unique',
            ],
            'PROCESSING': [
                {
                    'detect_language': {
                        'language_code': 'ru',
                        'delimiter': '~',
                        'delimited_position': -1,
                        'model_path': '/path/fasttext-lid.176.bin',
                    },
                },
                'remove_accents',
            ],
            'POST_PROCESSING': [
                'shuffle',
            ],
            'CACHE_DIR': '/cache/tdc',
        }

        with patch('builtins.open', mock_open(read_data=read_data)) as mock_file:
            result = load_config(path)
            mock_file.assert_called_with(path)

        assert result == should_be


class TestGetLinePiece:
    def test__no_delimiter(self):
        text = 'Line about nine'
        delimiter = None

        assert get_line_piece(text, delimiter, -1) == text
        assert get_line_piece(text, delimiter, 0) == text
        assert get_line_piece(text, delimiter, 1) == text
        assert get_line_piece(text, delimiter, 2) == text

    def test__delimiter__found(self):
        text = 'Column 1~Column #2~Description'
        delimiter = '~'

        assert get_line_piece(text, delimiter, -1) == 'Description'
        assert get_line_piece(text, delimiter, 0) == 'Column 1'

    def test__delimiter__not_found(self):
        text = 'Vodka&Balalayka&Big bear'
        delimiter = '~'

        assert get_line_piece(text, delimiter, -1) == text
        assert get_line_piece(text, delimiter, 0) == text
        assert get_line_piece(text, delimiter, 1) == text
        assert get_line_piece(text, delimiter, 2) == text
