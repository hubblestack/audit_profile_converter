from module_handler.audit_module_handler import AuditModuleHandler

class Misc(AuditModuleHandler):
    """
    Misc specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Misc arguments

        Example input for better understanding
            restrict_core_dumps:
              data:
                CentOS Linux-7:
                  function: check_core_dumps
              description: Ensure core dumps are restricted
        Args:
            m_key will be "CentOS Linux-7"
            m_data will be complete dictionary against m_key
        """
        function_name = m_data['function']
        result = {
            'function': function_name
        }

        if function_name in [
            'check_all_users_home_directory', 'check_users_own_their_home']:
            result['max_system_uid'] = m_data['args'][0]
        elif function_name in ['check_if_any_pkg_installed', 'restrict_permissions']:
            # Will be special handled by pkg module
            return None
        elif function_name == 'check_list_values':
            result['file_path'] = m_data['args'][0]
            result['match_pattern'] = m_data['args'][1]
            result['value_pattern'] = m_data['args'][2]
            result['grep_arg'] = m_data['args'][3]
            result['white_list'] = m_data['args'][4]
            result['black_list'] = m_data['args'][5]
            result['value_delimter'] = m_data['args'][6]
        elif function_name == 'check_directory_files_permission':
            result['path'] = m_data['args'][0]
            result['permission'] = m_data['args'][1]
        elif function_name == 'check_sshd_paramters':
            result['function'] = 'check_sshd_parameters'
            result['pattern'] = m_data['args'][0]
            if 'kwargs' in m_data:
                if 'values' in m_data['kwargs']:
                    result['values'] = m_data['kwargs']['values']
                if 'comparetype' in m_data['kwargs']:
                    result['comparetype'] = m_data['kwargs']['comparetype']
        elif function_name == 'check_users_home_directory_permissions':
            if 'args' in m_data:
                result['max_allowed_permission'] = m_data['args'][0]
                result['except_for_users'] = m_data['args'][1]
        elif function_name == 'test_mount_attrs':
            result['mount_name'] = m_data['args'][0]
            result['attribute'] = m_data['args'][1]
            result['check_type'] = m_data['args'][2]
            
        return result
    
    def _prepare_comparator(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Grep arguments

        Example input for better understanding
            restrict_core_dumps:
              data:
                CentOS Linux-7:
                  function: check_core_dumps
              description: Ensure core dumps are restricted
        Args:
            m_key will be "CentOS Linux-7"
            m_data will be complete dictionary against m_key
        """
        return {
          'type': 'boolean',
          'match': True
        }

    def fetch_tag(self, block_id, single_block):
        """
        Return first tag found in single block

        Note: If this impl doesn't work for some module.
        Define this method in respective module impl
        """
        for _, pdata in single_block['data'].items():
            return pdata['tag']