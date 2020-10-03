import os
import shutil

from .exceptions import TDSFileExistsError, TDSTypeError, TDSValueError
from .processors import processors_dict, processors_types


def check_output_file_not_exists(path: str):
    if os.path.exists(path):
        raise TDSFileExistsError(f'Output file already exists: {path}')


def validate_config(config: dict):
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
            raise TDSValueError(f'Missing required configuration parameter: {param}')

    for param_key, param_obj in config.items():
        if param_key not in parameter_types:
            raise TDSValueError(f'Unknown config parameter: {param_key}')

        if not isinstance(param_obj, parameter_types[param_key]):   # noqa # fixme
            raise TDSTypeError(f'Configuration parameter {param_key} must be a type of {parameter_types[param_key]}')


def validate_processors(config: dict):
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
                raise TDSValueError(f'Processor {processor_name} for stage {stage_name} not found!')

            if processors_types[processor_name] != stage_type:
                raise TDSValueError(f'Processor {processor_name} for stage {stage_name} '
                                    f'must be a {stage_type}-typed processor')

            # try create processor for check errors in initialization
            try:
                proc = processors_dict[processor_name](**params)
            except TypeError as e:
                message = str(e)
                # FIXME: hack for tell processor name
                message = message.replace('__init__()', f'{processor_name} processor')
                message = f'{message} for __init__ method'
                raise TDSTypeError(message)


def validate_free_space(input_file: str, output_file: str):
    file_size = os.path.getsize(input_file)  # worst case: temp_file = output_file = input_file
    file_size *= 2.2    # peak: (temp_file + output_file) * 1,1

    output_dir = os.path.dirname(output_file)
    free_space = shutil.disk_usage(output_dir).free

    if file_size > free_space:
        free_space = free_space // 1024 ** 2
        file_size = file_size // 1024 ** 2
        raise TDSOSError(f'Not enough disk space! Need: {file_size} MB, free: {free_space} MB')
