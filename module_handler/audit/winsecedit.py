from module_handler.audit_module_handler import ModuleHandler

class WinSecedit(ModuleHandler):
    """
    WinSecedit specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data):
        """
        Prepare WinSecedit arguments

        Example input for better understanding
            password_history_size:
              data:
                'Microsoft Windows Server 2012*':
                  - 'PasswordHistorySize':
                      tag: CIS-1.1.1
                      match_output: '10'
                      value_type: 'more'
              # Changing this to 10 as per PCI 8.2.3
              description: (l1) ensure 'enforce password history' is set to '10 or more password(s)'
        Args:
            m_key will be "PasswordHistorySize"
            m_data will be complete dictionary against m_key
        """
        result = {
            'name': m_key
        }
        result['value_type'] = m_data['value_type']

        return result
    
    def _prepare_comparator(self, m_key, m_data):
        """
        Prepare WinSecedit arguments

        Example input for better understanding
            password_history_size:
              data:
                'Microsoft Windows Server 2012*':
                  - 'PasswordHistorySize':
                      tag: CIS-1.1.1
                      match_output: '10'
                      value_type: 'more'
              # Changing this to 10 as per PCI 8.2.3
              description: (l1) ensure 'enforce password history' is set to '10 or more password(s)'
        Args:
            m_key will be "PasswordHistorySize"
            m_data will be complete dictionary against m_key
        """
        result = {
            'type': 'dict',
            'match': {
                'sec_value': {
                    'type': 'list',
                    'match': [m_data['match_output']]
                }
            }
        }
        return result
