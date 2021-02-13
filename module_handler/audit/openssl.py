from module_handler.audit_module_handler import AuditModuleHandler

class Openssl(AuditModuleHandler):
    """
    Openssl specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Grep arguments

        Example input for better understanding
            openssl:
              google:
                data:
                  tag: 'CERT-001'             # tag (required)
                  endpoint: 'www.google.com'  # required if file is not defined
                  file: null                  # /path/to/the/pem/file (required if endpoint is not defined)
                  port: 443                   # required only if both
                                              #       - endpoint is defined
                                              #       - https is not configured on port 443
                  not_after: 30                # minimum number of days until expiration (default value: 0)
                                              # the check is failed if the certificate expires in less then 30 days
                  not_before: 10               # number of days until the ceriticate becomes valid (default value: 0)
                                              # the check is failed if the certificate becomes valid in more then 10 days
                  fail_if_not_before: True     # fails the check if the certificate is not valid yet
                description: 'google certificate'
        Args:
            m_key will be "/etc/yum.conf"
            m_data will be complete dictionary against m_key
        """
        result = {
            
        }
        if 'pattern' in m_data:
            result['pattern'] = m_data['pattern']
        if 'grep_args' in m_data:
            result['flags'] = m_data['grep_args']

        return result
    
    def _prepare_comparator(self, m_key, m_data, block_tag, is_whitelist=True):
        """
        Prepare Openssl arguments

        Example input for better understanding
            activate_gpg_check:
                data:
                    CentOS Linux-7:
                    - '/etc/yum.conf':
                        match_output: gpgcheck=1
                        pattern: ^gpgcheck
                        tag: CIS-1.2.3

        Args:
            m_key will be "/etc/yum.conf"
            m_data will be complete dictionary against m_key
        """
        result = {'type': 'string'}
        if 'match_output' in m_data:
            result['match'] = m_data['match_output']
        else:
            # True for any found
            result['match'] = ".*"
            result['is_regex'] = True

        # check presence and True value
        if 'match_on_file_missing' in m_data and m_data['match_on_file_missing']:
            result['success_on_error'] = ['file_not_found']
        if 'match_output_regex' in m_data and m_data['match_output_regex']:
            result['is_regex'] = True
        if 'match_output_multiline' in m_data and m_data['match_output_multiline']:
            result['is_multiline'] = True
        
        return result

    def fetch_tag(self, block_id, single_block):
        """
        Return first tag found in single block

        Note: If this impl doesn't work for some module.
        Define this method in respective module impl
        """
        if 'tag' in single_block['data']:
            return single_block['data']['tag']
