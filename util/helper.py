import os
import logging
import yaml
import json
import ruamel.yaml

log = logging.getLogger(__name__)

def get_file_list(folder):
    """
    Get files list recursively under a folder
    """
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames]

def read_file(filepath):
    data = None
    with open(filepath, 'r') as file:
        data = file.read().replace('\n', '')
    return data

def load_yaml(filepath):
    """
    Load yaml file
    
    Arguments:
        filepath {str} -- Actual filepath of profile file
    Returns:
        [dict] -- Dictionary representation for yaml
    """
    log.info('Loading yaml file: %s', filepath)
    # validating physical file existance
    if not filepath or not os.path.isfile(filepath):
        raise FileNotFoundError('Could not find file: {0}'.format(filepath))

    yaml_data = None
    with open(filepath, 'r') as file_handle:
        # yaml_data = ruamel.yaml.round_trip_load(file_handle, preserve_quotes=True)
        yaml_data = yaml.safe_load(file_handle)

    return yaml_data

def save_file(filepath, content):
    parent_dir = os.path.dirname(filepath)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    with open(filepath, "w") as download_file:
        yaml.safe_dump(content, download_file, default_flow_style=False)
        # ruamel.yaml.round_trip_dump(content, download_file, explicit_start=True)
