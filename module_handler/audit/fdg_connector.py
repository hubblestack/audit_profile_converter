from module_handler.audit_module_handler import AuditModuleHandler

class FdgConnector(AuditModuleHandler):
    """
    FDG Connector specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Fdg-connector arguments

        Example input for better understanding
            fdg:
              check_ports_via_osquery:
                data:
                  '*':
                    fdg_file: 'salt://hubblestack_nova_profiles/fdg/blacklisted_services.fdg'
                    tag: BETA-0001
                description: Check that rsh, samba or telnet servers are not running
        Args:
            m_key will be '*'
            m_data will be complete dictionary against m_key
        """
        result = {
            'fdg_file': m_data['fdg_file']
        }
        if 'starting_chained' in m_data: 
            result['starting_chained'] = m_data['starting_chained']
        if 'true_for_success' in m_data:
            result['true_for_success'] = m_data['true_for_success']
        if 'use_status' in m_data:
            result['use_status'] = m_data['use_status']
        
        return result
    
    def _prepare_comparator(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Fdg-connector arguments

        Example input for better understanding
            fdg:
              check_ports_via_osquery:
                data:
                  '*':
                    fdg_file: 'salt://hubblestack_nova_profiles/fdg/blacklisted_services.fdg'
                    tag: BETA-0001
                description: Check that rsh, samba or telnet servers are not running
        Args:
            m_key will be '*'
            m_data will be complete dictionary against m_key
        """
        result = {
            'type': 'boolean',
            'match': True
        }
        return result

    def fetch_tag(self, block_id, single_block):
        """
        custom impl for fetch_tag
        """
        for _, pdata in single_block['data'].items():
            if 'tag' in pdata:
                return pdata['tag']
