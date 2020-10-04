import os
import shutil

from textdatasetcleaner.exceptions import TDCFileExistsError, TDCOSError, TDCTypeError, TDCValueError
from textdatasetcleaner.processors import processors_dict, processors_types


def check_output_file_not_exists(path: str) -> None:
    if os.path.exists(path):
        raise TDCFileExistsError(f'Output file already exists: {path}')


def validate_config(config: dict) -> None:
    required_parameters = ['PRE_PROCESSING', 'PROCESSING', 'POST_PROCESSING']
    # required + optional
    parameter_types = {
        'PRE_PROCESSING': list,
        'PROCESSING': list,
        'POST_PROCESSING': list,
        'CACHE_DIR': str,
    }

    for param in required_parameters:
        if param not in config:
            raise TDCValueError(f'Missing required configuration parameter: {param}')

    for param_key, param_obj in config.items():
        if param_key not in parameter_types:
            raise TDCValueError(f'Unknown config parameter: {param_key}')

        if not isinstance(param_obj, parameter_types[param_key]):
            raise TDCTypeError(f'Configuration parameter {param_key} must be a type of {parameter_types[param_key]}')


def validate_processors(config: dict) -> None:
    stage_types = {
        'PRE_PROCESSING': 'file',
        'PROCESSING': 'line',
        'POST_PROCESSING': 'file',
    }

    for stage_name, stage_type in stage_types.items():
        for processor in config[stage_name]:
            params = {}
            processor_name = processor
            if isinstance(processor, dict):
                # HACK: processor with parameters for __init__
                processor_name = list(processor)[0]
                params = processor[processor_name]

            if processor_name not in processors_types.keys():
                raise TDCValueError(f'Processor {processor_name} for stage {stage_name} not found!')

            if processors_types[processor_name] != stage_type:
                msg = f'Processor {processor_name} for stage {stage_name} must be a {stage_type}-typed processor'
                raise TDCValueError(msg)

            # try create processor for check errors in initialization
            try:
                processors_dict[processor_name](**params)
            except TypeError as exc:
                message = str(exc)
                # FIXME: hack for tell processor name
                message = message.replace('__init__()', f'{processor_name} processor')
                message = f'{message} for __init__ method'
                raise TDCTypeError(message)


def validate_free_space(input_file: str, output_file: str) -> None:
    file_size = 2.2  # peak: (temp_file + output_file) * 1,1
    file_size *= os.path.getsize(input_file)  # worst case: temp_file = output_file = input_file

    output_dir = os.path.dirname(output_file)
    free_space = shutil.disk_usage(output_dir).free

    if file_size > free_space:
        free_space = free_space // 1024 ** 2
        file_size = file_size // 1024 ** 2
        raise TDCOSError(f'Not enough disk space! Need: {file_size} MB, free: {free_space} MB')
