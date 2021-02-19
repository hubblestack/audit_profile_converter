from abc import ABC, abstractmethod

import os
import logging
import yaml

import util.helper as helper

log = logging.getLogger(__name__)

class FdgModuleHandler(ABC):
    """
    Base class for module specific implementation
    """

    def __init__(self, report_handler, block_id, module_name, function_name, module_block):
        self._report_handler = report_handler
        self._block_id = block_id
        self._module_name = module_name
        self._function_name = function_name
        self._module_block = module_block

    def convert(self):
        converted = self._build_initial_structure()
                
        any_issue = True
        prepared_args = self._prepare_args()
        if prepared_args:
            any_issue = False
            converted[self._block_id]['args'] = prepared_args
        comparator_args = self._prepare_comparator()
        if comparator_args:
            any_issue = False
            converted[self._block_id]['comparator'] = self._prepare_comparator()

        if any_issue:
            log.error('Something unexpected happened: block_id={0}'.format(self._block_id))
            return {}

        self._build_end_structure(converted)

        if prepared_args and 'temp' in prepared_args and prepared_args['temp'] is True:
            return converted

        self._report_handler.write(
            True, 
            {self._block_id: 
                self._module_block
            },
            converted
        )
        return converted

    @abstractmethod
    def _prepare_args(self):
        pass
    def _prepare_comparator(self):
        # optional comparator for fdg modules
        # modules has to implement, if they want
        return None
    
    def get_module_name(self):
        """
        To get module name.
        IN some cases, we have renamed module names. 
        In that case, respective module impl has to define this method
        """
        return self._module_name

    def _build_initial_structure(self):
        return {self._block_id: {
          'module': self.get_module_name()
        }}

    def _build_end_structure(self, result):
        if 'xpipe_on_true' in self._module_block:
            result[self._block_id]['xpipe_on_true'] = self._module_block['xpipe_on_true']
        if 'xpipe_on_false' in self._module_block:
            result[self._block_id]['xpipe_on_false'] = self._module_block['xpipe_on_false']
        if 'pipe_on_true' in self._module_block:
            result[self._block_id]['pipe_on_true'] = self._module_block['pipe_on_true']
        if 'pipe_on_false' in self._module_block:
            result[self._block_id]['pipe_on_false'] = self._module_block['pipe_on_false']
        if 'xpipe' in self._module_block:
            result[self._block_id]['xpipe'] = self._module_block['xpipe']
        if 'pipe' in self._module_block:
            result[self._block_id]['pipe'] = self._module_block['pipe']
