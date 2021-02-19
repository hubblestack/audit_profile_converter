from module_handler.fdg_module_handler import FdgModuleHandler

class Process(FdgModuleHandler):
    """
    Process specific conversion steps
    """
    def __init__(self, report_handler, block_id, module_name, function_name, module_block):
        super().__init__(report_handler, block_id, module_name, function_name, module_block)

    def _prepare_args(self):
        """
        Prepare Process arguments

        Example input for better understanding
            terminate_chaining_docker_not_running:
                module: process.print_string
                args:
                  - 'docker not running {0}'
        """
        if self._function_name == 'print_string':
            return {
                'function': 'print_string',
                'starting_string': self._module_block['args'][0]
            }
        return None

    def get_module_name(self):
        # newer module name
        return 'util'
