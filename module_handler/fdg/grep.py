from module_handler.fdg_module_handler import FdgModuleHandler

class Grep(FdgModuleHandler):
    """
    Grep specific conversion steps
    """
    def __init__(self, report_handler, block_id, module_name, function_name, module_block):
        super().__init__(report_handler, block_id, module_name, function_name, module_block)

    def _prepare_args(self):
        """
        Prepare Grep arguments

        Example input for better understanding
            check_count:
              module: grep.stdin
              args:
                - "count': u'0'"

        """
        if self._function_name == 'stdin':
            return self._stdin()
        return None

    def _stdin(self):
        if 'args' in self._module_block:
            return {
                'pattern': self._module_block['args'][0]
            }
        return None