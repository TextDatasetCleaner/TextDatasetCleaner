#!/usr/bin/python3

import click

from .loaders import load_config
from .validators import validate_config, validate_processors


@click.command()
@click.option('-c', '--config', required=True, type=click.Path(exists=True, readable=True, file_okay=True),
              help='Path to config file')
def run(config: str):
    configuration = load_config(config)
    validate_config(configuration)
    validate_processors(configuration)
    print(configuration)
