from module_handler.module_converter import ModuleConverter

class WinAuditPol(ModuleConverter):
    """
    WinAuditpol specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data):
        """
        Prepare WinAuditpol arguments

        Example input for better understanding
            Audit Credential Validation :
              data:
                'Microsoft Windows Server 2012*':
                  - 'Credential Validation':
                      tag: CIS-17.1.1
                      match_output: 'Success and Failure'
                      value_type: 'equal'
              description: (l1) ensure 'audit credential validation' is set to 'success and failure'
        Args:
            m_key will be 'Credential Validation'
            m_data will be complete dictionary against m_key
        """
        return {
            'name': m_key
        }
    
    def _prepare_comparator(self, m_key, m_data):
        """
        Prepare WinAuditpol arguments

        Example input for better understanding
            Audit Credential Validation :
              data:
                'Microsoft Windows Server 2012*':
                  - 'Credential Validation':
                      tag: CIS-17.1.1
                      match_output: 'Success and Failure'
                      value_type: 'equal'
              description: (l1) ensure 'audit credential validation' is set to 'success and failure'
        Args:
            m_key will be 'Credential Validation'
            m_data will be complete dictionary against m_key
        """
        result = {
            'type': 'dict',
            'match': {
                m_key: m_data['match_output']
            }
        }
        return result
