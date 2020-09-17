#!/usr/bin/python3

import click

from .helpers import load_config
from .loaders import Loader
from .validators import check_output_file_not_exists, validate_config, validate_free_space, validate_processors


@click.command()
@click.option('-c', '--config_file', type=click.Path(exists=True, resolve_path=True, readable=True, file_okay=True),
              required=True, help='Path to config file')
@click.option('-i', '--input_file', type=click.Path(exists=True, resolve_path=True, readable=True,  file_okay=True),
              required=True, help='Input file to processing')
@click.option('-o', '--output_file', type=click.Path(resolve_path=True, writable=True, file_okay=True),
              required=True, help='Output file to save results')  # FIXME: `exists=False` not worked
def run(config_file: str, input_file: str, output_file: str):
    check_output_file_not_exists(output_file)
    validate_free_space(input_file, output_file)

    config = load_config(config_file)
    validate_config(config)
    validate_processors(config)

    # create Loader
    ldr = Loader(config, input_file, output_file)
    # start pre processing
    ldr.pre_processing()

    print(config)
