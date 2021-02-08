from module_handler.audit_module_handler import AuditModuleHandler

class Systemctl(AuditModuleHandler):
    """
    Systemctl specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data):
        """
        Prepare Systemctl arguments

        Example input for better understanding
            rsyslog_enabled:
                data:
                    CentOS Linux-7:
                    - rsyslog:
                        tag: CIS-4.2.1.1
                description: Ensure rsyslog Service is enabled
        Args:
            m_key will be "rsyslog"
            m_data will be complete dictionary against m_key
        """
        return {
            'name': m_key
        }
    
    def _prepare_comparator(self, m_key, m_data):
        """
        Prepare Systemctl arguments

        Example input for better understanding
            rsyslog_enabled:
                data:
                    CentOS Linux-7:
                    - rsyslog:
                        tag: CIS-4.2.1.1
                description: Ensure rsyslog Service is enabled

        Args:
            m_key will be "rsyslog"
            m_data will be complete dictionary against m_key
        """
        result = {
          'type': 'list',
          'match_any': [{
              'name': m_key,
              'enabled': True
          }]
        }
        
        return result

    def get_module_name(self):
        # we clubbed systemctl to service module
        return 'service'