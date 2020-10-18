from unittest.mock import MagicMock, patch

from pytest import mark, raises

from textdatasetcleaner.exceptions import TDCFileExistsError, TDCTypeError, TDCValueError
from textdatasetcleaner.validators import check_output_file_not_exists, validate_config


class TestCheckOutputFileNotExists:
    def test__file_not_exists(self):
        assert check_output_file_not_exists('/some/unknown/file') is None

    def test__file_exists(self):
        path = '/some/known/file'

        with patch('os.path.exists', MagicMock(return_value=True)) as mock:
            with raises(TDCFileExistsError):
                assert check_output_file_not_exists(path) is None
                mock.assert_called_with(path)


class TestValidateConfig:
    @mark.parametrize(
        'config',
        [
            {},
            {'PRE_PROCESSING': []},
            {'PRE_PROCESSING': [], 'PROCESSING': []},
        ],
    )
    @mark.parametrize(
        'missed',
        [
            'PRE_PROCESSING',
            'PROCESSING',
            'POST_PROCESSING',
        ],
    )
    def test__miss_param(self, config: dict, missed: str):
        with raises(TDCValueError) as exc_info:
            validate_config(config)

            assert exc_info.value.args[0] == f'Missing required configuration parameter: {missed}'

    @mark.parametrize(
        'config',
        [
            {'PRE_PROCESSING': int, 'PROCESSING': [], 'POST_PROCESSING': [], 'CACHE_DIR': str},
            {'PRE_PROCESSING': [], 'PROCESSING': int, 'POST_PROCESSING': [], 'CACHE_DIR': str},
            {'PRE_PROCESSING': [], 'PROCESSING': [], 'POST_PROCESSING': int, 'CACHE_DIR': str},
            {'PRE_PROCESSING': [], 'PROCESSING': [], 'POST_PROCESSING': [], 'CACHE_DIR': int},
        ],
    )
    @mark.parametrize(
        'param',
        [
            'PRE_PROCESSING',
            'PROCESSING',
            'POST_PROCESSING',
            'CACHE_DIR',
        ],
    )
    @mark.parametrize(
        'must_be_type',
        [
            list,
            list,
            list,
            str,
        ],
    )
    def test__unknown_type(self, config: dict, param: str, must_be_type: type):
        with raises(TDCTypeError) as exc_info:
            validate_config(config)

            assert exc_info.value.args[0] == f'Configuration parameter {param} must be a type of {must_be_type}'
