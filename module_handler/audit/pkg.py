from module_handler.audit_module_handler import ModuleHandler

class Pkg(ModuleHandler):
    """
    Pkg specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data):
        """
        Prepare Pkg arguments

        Example input for better understanding
            tcp_wrappers:
              data:
                CentOS Linux-7:
                - tcp_wrappers: CIS-3.4.1
              description: Ensure TCP Wrappers is installed
        Args:
            m_key will be "tcp_wrappers"
            m_data will be complete dictionary against m_key
        """
        return {
            'name': m_key
        }
    
    def _prepare_comparator(self, m_key, m_data):
        """
        Prepare Pkg arguments

        Example input for better understanding
            tcp_wrappers:
              data:
                CentOS Linux-7:
                - tcp_wrappers: CIS-3.4.1
              description: Ensure TCP Wrappers is installed

        Args:
            m_key will be "tcp_wrappers"
            m_data will be complete dictionary against m_key
        """
        result = {
          'type': 'dict',
          'match_key_any': [m_key]
        }
        
        return result

    def fetch_tag(self, block_id, single_block):
        """
        Return first tag found in single block
        """
        for _, pdata in single_block['data'].items():
            for impls in pdata:
                for _, m_data in impls.items():
                    return m_data
