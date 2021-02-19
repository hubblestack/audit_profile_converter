from module_handler.fdg_module_handler import FdgModuleHandler

class CommandLineParser(FdgModuleHandler):
    """
    CommandLineParser specific conversion steps
    """
    def __init__(self, report_handler, block_id, module_name, function_name, module_block):
        super().__init__(report_handler, block_id, module_name, function_name, module_block)

    def _prepare_args(self):
        """
        Prepare CommandLineParser arguments

        Example input for better understanding
            command_line_parser:
              module: command_line_parser.parse_cmdline
              args:
                - key_aliases: ["config-file"]
                  delimiter: "="
              xpipe:
                grep_output
        """
        if self._function_name == 'parse_cmdline':
            return self._handle_cmdline()

        return None

    def _handle_cmdline(self):
        result = {}
        if 'key_aliases' in self._module_block['args'][0]:
            result['key_aliases'] = self._module_block['args'][0]['key_aliases']
        if 'delimiter' in self._module_block['args'][0]:
            result['delimiter'] = self._module_block['args'][0]['delimiter']
        return result
