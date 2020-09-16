import yaml


def load_config(path: str):
    return yaml.safe_load(open(path))
