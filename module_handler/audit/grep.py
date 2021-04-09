from module_handler.audit_module_handler import AuditModuleHandler

class Grep(AuditModuleHandler):
    """
    Grep specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Grep arguments

        Example input for better understanding
            activate_gpg_check:
                data:
                    CentOS Linux-7:
                    - '/etc/yum.conf':
                        match_output: gpgcheck=1
                        pattern: ^gpgcheck
                        tag: CIS-1.2.3
        Args:
            m_key will be "/etc/yum.conf"
            m_data will be complete dictionary against m_key
        """
        result = {
            'path': m_key
        }
        if 'pattern' in m_data:
            pattern = m_data['pattern']
            if ' ' in pattern and '"' not in pattern:
                pattern = f'"{pattern}"'
            result['pattern'] = pattern
        if 'grep_args' in m_data:
            result['flags'] = m_data['grep_args']

        return result
    
    def _prepare_comparator(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Grep arguments

        Example input for better understanding
            activate_gpg_check:
                data:
                    CentOS Linux-7:
                    - '/etc/yum.conf':
                        match_output: gpgcheck=1
                        pattern: ^gpgcheck
                        tag: CIS-1.2.3

        Args:
            m_key will be "/etc/yum.conf"
            m_data will be complete dictionary against m_key
        """
        result = {'type': 'string'}
        if 'match_output' in m_data:
            result['match'] = '.*' + m_data['match_output'] + '.*'
            result['is_regex'] = True
        else:
            # True for any found
            result['match'] = ".*"
            result['is_regex'] = True

        # check presence and True value
        if 'match_on_file_missing' in m_data and m_data['match_on_file_missing']:
            result['success_on_error'] = ['file_not_found']
        if 'match_output_regex' in m_data and m_data['match_output_regex']:
            result['is_regex'] = True
        if 'match_output_multiline' in m_data and m_data['match_output_multiline']:
            result['is_multiline'] = True
        
        return result
