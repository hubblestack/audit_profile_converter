from module_handler.audit_module_handler import AuditModuleHandler

class WinPkg(AuditModuleHandler):
    """
    WinPkg specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare WinPkg arguments

        Example input for better understanding
            EMET 5.5 :
              data:
                'Microsoft Windows Server 2012*':
                  - 'EMET 5.5':
                      tag: CIS-18.9.24.1
                      match_output: '5.4'
                      value_type: 'more'
              description: (l1) ensure 'emet 5.5' or higher is installed
        Args:
            m_key will be 'EMET 5.5'
            m_data will be complete dictionary against m_key
        """
        return {
            'name': m_key
        }
    
    def _prepare_comparator(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare WinPkg arguments

        Example input for better understanding
            EMET 5.5 :
              data:
                'Microsoft Windows Server 2012*':
                  - 'EMET 5.5':
                      tag: CIS-18.9.24.1
                      match_output: '5.4'
                      value_type: 'more'
              description: (l1) ensure 'emet 5.5' or higher is installed
        Args:
            m_key will be 'EMET 5.5'
            m_data will be complete dictionary against m_key
        """
        # default value of op (equal)
        operator = '=='
        if m_data['value_type'] == 'more':
            operator = '>='
        elif m_data['value_type'] == 'less':
            operator = '<='
        match_output = m_data['match_output']

        result = {
            'type': 'dict',
            'match': {
                'package_version': {
                    'type': "version",
                    'match':
                      f"{operator} {match_output}"
                }
            }
        }
        return result
