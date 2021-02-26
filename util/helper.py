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

    # read comments from top
    comments = load_yaml_comments(filepath)
    return (yaml_data, comments)

def load_yaml_comments(filepath):
    comments = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip().startswith('#'):
                comments.append(line.replace('\n', ''))
            elif line.strip() == '':
                continue
            else:
                break
    return comments

def save_file(filepath, content, comments):
    parent_dir = os.path.dirname(filepath)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    file_mode = 'w'
    if comments:
        with open(filepath, file_mode = 'w') as the_file:
            file_mode = 'a'
            for comment in comments:
                the_file.write(comment)
                the_file.write('\n')
            the_file.write('\n')

    with open(filepath, file_mode) as download_file:
        yaml.safe_dump(content, download_file, default_flow_style=False, sort_keys=False)

