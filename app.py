import logging
logging.basicConfig(level=logging.INFO)

from workflow.converter import Converter

folder = './test_data/profiles'
report_folder = './test_data/report'
template_folder = './template'

converter = Converter(folder, report_folder, template_folder)

converter.convert()

print('Done')