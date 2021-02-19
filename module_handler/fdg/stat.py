from module_handler.fdg_module_handler import FdgModuleHandler

class Stat(FdgModuleHandler):
    """
    Stat specific conversion steps
    """
    def __init__(self, report_handler, block_id, module_name, function_name, module_block):
        super().__init__(report_handler, block_id, module_name, function_name, module_block)

    def _prepare_args(self):
        """
        Prepare Stat arguments

        Example input for better understanding
            get_stats:
              module: stat.get_stats
              pipe:
                match_stats

            OR

            match_stats:
              module: stat.match_stats
              args:
                - mode: 660
                  group: docker
                  uid: 0
                  user: root
                  allow_more_strict: True
                  match_on_file_missing: True 

        """
        if self._function_name == 'get_stats':
            if 'args' not in self._module_block or 'filepath' not in self._module_block['args'][0]:
                # temp status, incidation that do not count its result
                return {
                'temp': True
                }
            else:
                return {'path': self._module_block['args'][0]['filepath']}
        elif self._function_name == 'match_stats':
            return None
        return None

    def _prepare_comparator(self):
        if self._function_name == 'match_stats':
            return self._match_stats()
    def _match_stats(self):
        args = self._module_block['args'][0]
        result = {
          'type': 'dict',
          'match': {}
        }
        if 'uid' in args:
            result['match']['uid'] = args['uid']
        if 'user' in args:
            result['match']['user'] = args['user']
        if 'gid' in args:
            result['match']['gid'] = args['gid']
        if 'group' in args:
            result['match']['group'] = args['group'] 

        if 'mode' in args:
            result['match']['mode'] = {
                'type': 'file_permission',
                'match': {
                    'required_value': args['mode']
                }
            }

        if 'allow_more_strict' in args:
            result['match']['mode']['match']['allow_more_strict'] = args['allow_more_strict']

        if 'match_on_file_missing' in args and args['match_on_file_missing']:
            result['success_on_error'] = ['file_not_found']

        return result