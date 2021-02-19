from module_handler.fdg.osquery import Osquery
from module_handler.fdg.grep import Grep
from module_handler.fdg.stat import Stat
from module_handler.fdg.process import Process
from module_handler.fdg.ssl_certificate import SSLCertificate
from module_handler.fdg.commandlineparser import CommandLineParser

def get_module_handler(
        report_handler, block_id, module_name, function_name, module_block):
    handler = None
    if module_name == 'osquery':
        handler = Osquery
    elif module_name == 'grep':
        handler = Grep
    elif module_name == 'ssl_certificate':
        handler = SSLCertificate
    elif module_name == 'stat':
        handler = Stat
    elif module_name == 'process':
        handler = Process
    elif module_name == 'command_line_parser':
        handler = CommandLineParser

    if handler:
        return handler(
            report_handler, 
            block_id, 
            module_name, 
            function_name, 
            module_block
        )
    return None
