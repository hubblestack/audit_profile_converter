from module_handler.audit_module_handler import ModuleHandler

class Stat(ModuleHandler):
    """
    Stat specific conversion steps
    """
    def __init__(self, report_handler, module_name, module_block):
        super().__init__(report_handler, module_name, module_block)

    def _prepare_args(self, m_key, m_data):
        """
        Prepare Stat arguments

        Example input for better understanding
            grub_conf_own_perm:
              data:
                CentOS Linux-7:
                - /etc/grub2.cfg:
                    gid: 0
                    group: root
                    mode: 600
                    tag: CIS-1.4.1
                    uid: 0
                    user: root
                    allow_more_strict: True
              description: Ensure permissions on bootloader config are configured
        Args:
            m_key will be "/etc/grub2.cfg"
            m_data will be complete dictionary against m_key
        """
        return {
            'path': m_key
        }
    
    def _prepare_comparator(self, m_key, m_data):
        """
        Prepare Systemctl arguments

        Example input for better understanding
            grub_conf_own_perm:
              data:
                CentOS Linux-7:
                - /etc/grub2.cfg:
                    gid: 0
                    group: root
                    mode: 600
                    tag: CIS-1.4.1
                    uid: 0
                    user: root
                    allow_more_strict: True
              description: Ensure permissions on bootloader config are configured
        Args:
            m_key will be "/etc/grub2.cfg"
            m_data will be complete dictionary against m_key
        """
        result = {
          'type': 'dict',
          'match': {
              'uid': m_data['uid'],
              'user': m_data['user'],
              'gid': None if 'gid' not in m_data else m_data['gid'],
              'group': m_data['group'],
              'mode': {
                'type': 'file_permission',
                'match': {
                  'required_value': m_data['mode']
                }
              }
          }
        }

        if 'allow_more_strict' in m_data:
            result['match']['mode']['match']['allow_more_strict'] = m_data['allow_more_strict']

        if 'match_on_file_missing' in m_data and m_data['match_on_file_missing']:
            result['success_on_error'] = ['file_not_found']
        
        return result
