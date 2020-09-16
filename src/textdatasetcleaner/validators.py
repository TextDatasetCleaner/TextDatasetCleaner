from .processors import processors_dict


def validate_config(config: dict):
    required_parameters = ['PRE_PROCESSORS', 'PROCESSORS', 'POST_PROCESSORS']
    parameter_types = {
        'PRE_PROCESSORS': list,
        'PROCESSORS': list,
        'POST_PROCESSORS': list,
    }

    for param in required_parameters:
        if param not in config:
            # TODO: own exception
            raise ValueError(f'Missing required configuration parameter: {param}')

    for param, type_ in parameter_types.items():
        if not isinstance(config[param], type_):
            # TODO: own exception
            raise TypeError(f'Configuration parameter {param} must be a type of {type_}')


def validate_processors(config: dict):
    stage_types = {
        'PRE_PROCESSORS': 'file',
        'PROCESSORS': 'line',
        'POST_PROCESSORS': 'file',
    }

    for stage_name, stage_type in stage_types.items():
        for processor in config[stage_name]:
            if processor not in processors_dict.keys():
                raise ValueError(f'Processor {processor} for stage {stage_name} not found!')

            if processors_dict[processor].type != stage_type:
                raise ValueError(f'Processor {processor} for stage {stage_name} must be a {stage_type}-typed processor')
