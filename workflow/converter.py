import os
import logging

from module_handler.module_converter import ModuleConverter
from factory.module_converter_factory import get_module_handler
from report_handler.report_handler import ReportHandler
from util import helper

log = logging.getLogger(__name__)

class Converter:
    """
    Starting point of converter 
    """

    def __init__(self, folder, report_folder, template_folder):
        self._report_folder = report_folder
        self._folder = folder
        self._template_folder = template_folder

    def convert(self):
        profile_files = helper.get_file_list(self._folder)
        for profile_file in profile_files:
            report_handler = ReportHandler(
                self._report_folder, self._folder, profile_file, self._template_folder)

            self._yaml_dict = helper.load_yaml(profile_file)
            for mod_name, yaml_block in self._yaml_dict.items():
                module_handler = get_module_handler(
                    report_handler, mod_name, yaml_block)
                if not module_handler:
                    report_handler.add_unhandled()
                    log.error('Unhandled module: {0} in file: {1}'.format(mod_name, profile_file))
                    continue
                converted_yaml = module_handler.convert()

            report_handler.save()


    def get_module_type(self):
        pass