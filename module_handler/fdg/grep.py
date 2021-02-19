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
        elif self._function_name == 'file':
            return self._file()
        return None

    def _stdin(self):
        if 'args' in self._module_block:
            result = {
                'pattern': self._module_block['args'][0]
            }
            if 'kwargs' in self._module_block:
                if 'grep_args' in self._module_block['kwargs']:
                    result['flags'] = [self._module_block['kwargs']['grep_args']]
            return result
        return None

    def _file(self):
        if 'args' in self._module_block:
            result = {
                'path': self._module_block['args'][0],
                'pattern': [self._module_block['kwargs']['pattern']]
            }
            return result
        return None