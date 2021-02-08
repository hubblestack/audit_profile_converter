from abc import ABC, abstractmethod

import os
import logging
import yaml

import util.helper as helper

log = logging.getLogger(__name__)

class AuditModuleHandler(ABC):
    """
    Base class for module specific implementation
    """

    def __init__(self, report_handler, module_name, module_block):
        self._report_handler = report_handler
        self._module_name = module_name
        self._module_block = module_block

    def convert(self):
        converted_yaml = {}
        if ('whitelist' not in self._module_block and 
                'blacklist' not in self._module_block):
            # In some modules, whitelist/blacklist is not there
            # Simulating that behavior here, so that below code can work for all
            temp = self._module_block
            self._module_block = {}
            self._module_block['whitelist'] = temp

        if 'whitelist' in self._module_block:
            for block_id, single_block in self._module_block['whitelist'].items():
                converted_result = self._convert_helper(
                    block_id, single_block
                )
                converted_yaml = dict(list(converted_yaml.items()) + list(converted_result.items()))
        
        if 'blacklist' in self._module_block:
            for block_id, single_block in self._module_block['blacklist'].items():
                converted_result = self._convert_helper(
                    block_id, single_block, is_whitelist=False
                )
                converted_yaml = dict(list(converted_yaml.items()) + list(converted_result.items()))
        return converted_yaml

    def _convert_helper(self, block_id, single_block, is_whitelist=True):
        if self._is_skipped(single_block):
            self._report_handler.skipped({
                self._module_name: {block_id: single_block}})
            return {}
        converted = self._build_initial_structure(block_id, single_block, is_whitelist)
        for p_os, pdata in single_block['data'].items():
            osfinger_os = p_os.replace(' ', '*')
            single_os = {
                'filter': {
                    'grains': 'G@osfinger:{0}'.format(osfinger_os)
                },
                'module': self.get_module_name(),
                'items': []
            }
            if isinstance(pdata, list):
                for impls in pdata:
                    for m_key, m_data in impls.items():
                        prepared_args = self._prepare_args(m_key, m_data)
                        if prepared_args:
                            single_os['items'].append({
                                'args': prepared_args,
                                'comparator': self._prepare_comparator(m_key, m_data)
                            })
                        else:
                            log.error('Something unexpected happened: key={0}, val={1}'.format(m_key, m_data))
            else:
                prepared_args = self._prepare_args(p_os, pdata)
                if prepared_args:
                    single_os['items'].append({
                        'args': prepared_args,
                        'comparator': self._prepare_comparator(p_os, pdata)
                    })
                else:
                    log.error('Something unexpected happened: key={0}, val={1}'.format(p_os, pdata))

            converted[block_id]['implementations'].append(single_os)
        
        self._report_handler.write(
            is_whitelist, 
            {self._module_name: 
                {"whitelist" if is_whitelist else "blacklist": {
                    block_id: single_block}}
            },
            converted
        )
        return converted

    @abstractmethod
    def _prepare_args(self, m_key, m_data):
        pass
    @abstractmethod
    def _prepare_comparator(self, m_key, m_data):
        pass
    
    def get_module_name(self):
        """
        To get module name.
        IN some cases, we have renamed module names. 
        In that case, respective module impl has to define this method
        """
        return self._module_name

    def fetch_tag(self, block_id, single_block):
        """
        Return first tag found in single block

        Note: If this impl doesn't work for some module.
        Define this method in respective module impl
        """
        for _, pdata in single_block['data'].items():
            for impls in pdata:
                for _, m_data in impls.items():
                    if 'tag' in m_data:
                        return m_data['tag']

    def _build_initial_structure(self, block_id, single_block, is_whitelist=True):
        result = {block_id: {}}
        if 'description' in single_block:
            result[block_id]['description'] = single_block['description']
        result[block_id]['tag'] = self.fetch_tag(block_id, single_block)

        if not is_whitelist:
            result[block_id]['invert_result'] = True

        # this is here for ordering purpose.
        # else it could have been in top lines
        result[block_id]['implementations'] = []

        return result

    def _is_skipped(self, single_block):
        """
        To check if this block should be skipped or not
        """
        return 'control' in single_block
