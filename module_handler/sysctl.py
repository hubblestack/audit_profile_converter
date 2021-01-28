from module_handler.module_converter import ModuleConverter

class Sysctl(ModuleConverter):
    """
    Sysctl specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data):
        """
        Prepare Sysctl arguments

        Example input for better understanding
            restrict_suid_core_dumps:
              data:
                CentOS Linux-7:
                - fs.suid_dumpable:
                    match_output: '0'
                    tag: CIS-1.5.1
              description: Ensure core dumps are restricted
        Args:
            m_key will be "fs.suid_dumpable"
            m_data will be complete dictionary against m_key
        """
        return {
            'name': m_key
        }
    
    def _prepare_comparator(self, m_key, m_data):
        """
        Prepare Sysctl arguments

        Example input for better understanding
            restrict_suid_core_dumps:
              data:
                CentOS Linux-7:
                - fs.suid_dumpable:
                    match_output: '0'
                    tag: CIS-1.5.1
              description: Ensure core dumps are restricted

        Args:
            m_key will be "fs.suid_dumpable"
            m_data will be complete dictionary against m_key
        """
        result = {'type': 'dict'}
        if 'match_output' in m_data:
            result['match'] = {
              m_key: m_data['match_output']
            }

        # check presence and True value
        if 'match_on_file_missing' in m_data and m_data['match_on_file_missing']:
            result['success_on_error'] = ['file_not_found']
        if 'match_output_regex' in m_data and m_data['match_output_regex']:
            result['is_regex'] = True
        if 'match_output_multiline' in m_data and m_data['match_output_multiline']:
            result['is_multiline'] = True
        
        return result

