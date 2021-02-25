from module_handler.audit_module_handler import AuditModuleHandler

class WinSecedit(AuditModuleHandler):
    """
    WinSecedit specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data, block_tag, is_whitelist=True):
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
    
    def _prepare_comparator(self, m_key, m_data, block_tag, is_whitelist=True):
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
        key_name = 'sec_value'
        if not is_whitelist:
            key_name = 'coded_sec_value'
        elif 'value_type' in m_data and m_data['value_type'] in ['more', 'less']:
            key_name = 'coded_sec_value'
        match_output_list = []
        for mitem in m_data['match_output'].split(','):
            if block_tag in ['CIS-2.3.7.4']:
                mitem = mitem.replace('"', '')
                match_output_list.append(mitem)
            else:
                match_output_list.append(mitem.strip())
        result = {
            'type': 'dict',
            'match': {
                key_name: {
                    'type': 'list',
                    'match_all': match_output_list,
                    'ignore_case': True
                }
            }
        }

        # custom handling for more, less
        if m_data['value_type'] in ['more', 'less']:
            op = ''
            if m_data['value_type'] == 'more':
                op = '>='
            elif m_data['value_type'] == 'less':
                op = '<='
            result['match'][key_name] = {
                'type': 'number',
                'match': op + m_data['match_output']
            }

        ## hack, custom handling
        if block_tag in ['ADOBEW-00056', 'ADOBEW-00072', 'CIS-2.3.10.10', 'CIS-2.3.11.7']:
            result = {
                'type': 'dict',
                'match': {
                    'coded_sec_value': m_data['match_output']
                }
            }
        if block_tag in ['CIS-2.3.11.9', 'CIS-2.3.11.10']:
            result['match'][key_name]['match_all'] = [m_data['match_output']]
        if block_tag in ['CIS-2.2.5']:
            mapping = []
            for m in result['match'][key_name]['match_all']:
                mapping.append(self._get_mapping(m))
            result['match'][key_name]['match_all'] = mapping

        return result

    def _get_mapping(self, key):
        mapping = {
            'Administrators': '*S-1-5-19',
            'LOCAL SERVICE': '*S-1-5-20',
            'NETWORK SERVICE': '*S-1-5-32-544'
        }

        return mapping.get(key)
