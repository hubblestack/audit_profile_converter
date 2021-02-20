import logging
from datetime import datetime
from util.osfinger_mapper import OsfingerMapper

log_file = '{:%Y-%m-%d-%H-%M-%S}.log'.format(datetime.now())
logging.basicConfig(filename=log_file,level=logging.INFO)
logger = logging.getLogger(__name__)

from workflow.converter import Converter
template_folder = './template'
static_mapping_data = './data/mapping.json'

## Change below variables for different paths
folder = './test_data/profiles'
report_folder = './test_data/report'
dest_profile_folder = './test_data/converted'

osfinger_mapper = OsfingerMapper(static_mapping_data)
converter = Converter(folder, dest_profile_folder, report_folder, template_folder, osfinger_mapper)

converter.convert()

print('Done')