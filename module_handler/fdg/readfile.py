from module_handler.fdg_module_handler import FdgModuleHandler

class Readfile(FdgModuleHandler):
    """
    Readfile specific conversion steps
    """
    def __init__(self, report_handler, block_id, module_name, function_name, module_block):
        super().__init__(report_handler, block_id, module_name, function_name, module_block)

    def _prepare_args(self):
        """
        Prepare Readfile arguments

        Example input for better understanding
            read_default_file:
              module: readfile.json
              args:
                  - "/etc/docker/daemon.json"
              kwargs:
                  subkey: "tlskey"
              pipe_on_true:
                get_stats

        """
        if self._function_name == 'json':
            return self._json()
        return None

    def _json(self):
        if 'args' in self._module_block:
            result = {
                'path': self._module_block['args'][0],
                'subkey': self._module_block['kwargs']['subkey']
            }
            if 'sep' in self._module_block['kwargs']:
                result['sep'] = self._module_block['kwargs']['sep']

            return result
        return None

    