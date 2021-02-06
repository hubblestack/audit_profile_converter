from module_handler.audit_module_handler import ModuleHandler

class WinReg(ModuleHandler):
    """
    WinReg specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data):
        """
        Prepare WinReg arguments

        Example input for better understanding
            Enable insecure guest logons:
              data:
                'Microsoft Windows Server 201[!2]*':  # This check is only applicable to >= Server 2016
                  - 'HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation\AllowInsecureGuestAuth':
                      tag: ADOBEW-00057
                      match_output: '0'
                      value_type: 'equal'
              description: Ensure 'Enable insecure guest logons' is set to 'Disabled'
        Args:
            m_key will be 'HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation\AllowInsecureGuestAuth'
            m_data will be complete dictionary against m_key
        """
        return {
            'name': m_key
        }
    
    def _prepare_comparator(self, m_key, m_data):
        """
        Prepare WinReg arguments

        Example input for better understanding
            Enable insecure guest logons:
              data:
                'Microsoft Windows Server 201[!2]*':  # This check is only applicable to >= Server 2016
                  - 'HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation\AllowInsecureGuestAuth':
                      tag: ADOBEW-00057
                      match_output: '0'
                      value_type: 'equal'
              description: Ensure 'Enable insecure guest logons' is set to 'Disabled'
        Args:
            m_key will be 'HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation\AllowInsecureGuestAuth'
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
                m_key: {
                  'type': "number",
                  'match': f"{operator} {match_output}"
                }
            }
        }
        return result
