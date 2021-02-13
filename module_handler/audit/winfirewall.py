from module_handler.audit_module_handler import AuditModuleHandler

class WinFirewall(AuditModuleHandler):
    """
    WinFirewall specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare WinReg arguments

        Example input for better understanding
            windows_firewall_domain_firewall_state:
              data:
                '*':
                  - 'Enabled':
                      tag: ADOBEW-00094
                      match_output: 'True'
                      value_type: 'domain'
              description: "Ensure 'Windows Firewall: Domain: Firewall state' is set to 'On (recommended)'"
        Args:
            m_key will be 'Enabled'
            m_data will be complete dictionary against m_key
        """
        return {
            'name': m_key,
            'value_type': m_data['value_type']
        }
    
    def _prepare_comparator(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare WinFirewall arguments

        Example input for better understanding
            windows_firewall_domain_firewall_state:
              data:
                '*':
                  - 'Enabled':
                      tag: ADOBEW-00094
                      match_output: 'True'
                      value_type: 'domain'
              description: "Ensure 'Windows Firewall: Domain: Firewall state' is set to 'On (recommended)'"
        Args:
            m_key will be 'Enabled'
            m_data will be complete dictionary against m_key
        """
        result = {
            'type': 'dict',
            'match': {
                'setting_value': {
                  'type': "string",
                  'match': [m_data['match_output']]
                }
            }
        }
        return result
