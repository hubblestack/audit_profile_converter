from module_handler.audit_module_handler import AuditModuleHandler

class Service(AuditModuleHandler):
    """
    Service specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Service arguments

        Example input for better understanding
            autofs:
              data:
                'Amazon Linux-2':
                - autofs: CIS-1.1.19
              description: Disable Automounting
        Args:
            m_key will be "autofs"
            m_data will be complete dictionary against m_key
        """
        return {
            'name': m_key
        }
    
    def _prepare_comparator(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Service arguments

        Example input for better understanding
            autofs:
              data:
                'Amazon Linux-2':
                - autofs: CIS-1.1.19
              description: Disable Automounting
        Args:
            m_key will be "autofs"
            m_data will be complete dictionary against m_key
        """
        return {
            'type': 'list',
            'match_any': [{
              'name': m_key,
              'running': True
            }]
        }

    def fetch_tag(self, block_id, single_block):
        """
        Return first tag found in single block
        """
        for _, pdata in single_block['data'].items():
            for impls in pdata:
                for _, m_data in impls.items():
                    return m_data
