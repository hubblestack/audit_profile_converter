import logging
from datetime import datetime

log_file = '{:%Y-%m-%d-%H-%M-%S}.log'.format(datetime.now())
logging.basicConfig(filename=log_file,level=logging.INFO)
logger = logging.getLogger(__name__)

from workflow.converter import Converter

folder = '/Users/gsingal/work/official/hubble/profiles/hubblestack_data-develop_1/'
# './test_data/profiles'

report_folder = './test_data/report'
template_folder = './template'
dest_profile_folder = './test_data/converted'

converter = Converter(folder, dest_profile_folder, report_folder, template_folder)

converter.convert()

print('Done')