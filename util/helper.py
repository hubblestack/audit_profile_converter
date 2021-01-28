import os
import logging
import yaml

log = logging.getLogger(__name__)

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
        yaml_data = yaml.safe_load(file_handle)

    return yaml_data

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
