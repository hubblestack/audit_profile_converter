import os
import logging

from module_handler.audit_module_handler import AuditModuleHandler
from module_handler.fdg_module_handler import FdgModuleHandler
from factory import audit_converter_factory
from factory import fdg_converter_factory
from report_handler.report_handler import ReportHandler
from util import helper

log = logging.getLogger(__name__)

class Converter:
    """
    Starting point of converter 
    """

    def __init__(self, folder, dest_profile_folder, report_folder, template_folder):
        self._report_folder = report_folder
        self._dest_profile_folder = dest_profile_folder
        self._folder = folder
        self._template_folder = template_folder

    def convert(self):
        profile_files = helper.get_file_list(self._folder)
        for profile_file in profile_files:
            if self.should_skip(profile_file):
                log.info(f'Not reading file: {profile_file}')
                continue
            report_handler = ReportHandler(
                self._report_folder, self._folder, profile_file, self._template_folder)

            # start working on single file
            yaml_dict = helper.load_yaml(profile_file)
            if not yaml_dict:
                log.info(f'No content in file: {profile_file}')
                continue

            if not self.is_fdg_file(profile_file):
                converted_yaml = self._handle_audit(yaml_dict, profile_file, report_handler)
            else:
                # handle fdg
                converted_yaml = self._handle_fdg(yaml_dict, profile_file, report_handler)

            target_file = self._get_target_filepath(profile_file)
            log.info(f'Writing target file: {target_file}')
            helper.save_file(target_file, converted_yaml)
            report_handler.save()

    def should_skip(self, filename):
        file_basename = os.path.basename(filename)
        return not (
            file_basename.endswith('.yaml') or
            file_basename.endswith('.yml') or
            file_basename.endswith('.fdg')
        ) or (
            'nebula' in filename or
            'pulsar' in filename or
            file_basename.startswith('top.') or
            'mask' in file_basename
        )


    def is_fdg_file(self, filename):
        return filename.endswith('.fdg')
    def _get_target_filepath(self, profile_file):
        relative_path = profile_file.split(self._folder)[1]
        result_path = f'{self._dest_profile_folder}{relative_path}'
        if not self._dest_profile_folder.endswith('/') and not relative_path.startswith('/'):
            result_path = f'{self._dest_profile_folder}/{relative_path}'
        return result_path

    def _handle_fdg(self, yaml_dict, profile_file, report_handler):
        converted = []
        for block_id, yaml_block in yaml_dict.items():
            mod_name = yaml_block['module'].split('.')[0]
            function_name = yaml_block['module'].split('.')[1]

            module_handler = fdg_converter_factory.get_module_handler(
                report_handler, block_id, mod_name, function_name, yaml_block)
            if not module_handler:
                report_handler.add_unhandled(mod_name)
                log.error('Unhandled module: {0} in file: {1}'.format(mod_name, profile_file))
                continue
            converted.append(module_handler.convert())

        return converted

    def _handle_audit(self, yaml_dict, profile_file, report_handler):
        converted = {}
        for mod_name, yaml_block in yaml_dict.items():
            module_handler = audit_converter_factory.get_module_handler(
                report_handler, mod_name, yaml_block)
            if not module_handler:
                report_handler.add_unhandled(mod_name)
                log.error('Unhandled module: {0} in file: {1}'.format(mod_name, profile_file))
                continue
            converted_result = module_handler.convert()
            converted = dict(list(converted.items()) + list(converted_result.items()))
            # converted.extend(module_handler.convert())
        return converted

    def get_module_type(self):
        pass

