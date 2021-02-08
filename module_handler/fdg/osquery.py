from module_handler.fdg_module_handler import FdgModuleHandler

class Osquery(FdgModuleHandler):
    """
    Osquery specific conversion steps
    """
    def __init__(self, report_handler, block_id, module_name, function_name, module_block):
        super().__init__(report_handler, block_id, module_name, function_name, module_block)

    def _prepare_args(self):
        """
        Prepare Osquery arguments

        Example input for better understanding
            main:
                module: osquery.query
                args:
                    - "SELECT DISTINCT CASE lp.address WHEN '0.0.0.0' THEN '127.0.0.1' WHEN '::' THEN '127.0.0.1' ELSE lp.address END as host_ip, lp.port as host_port FROM listening_ports AS lp WHERE lp.protocol=6 limit 500;"
                xpipe:
                    fetch_certificate_details
        """
        if self._function_name == 'query':
            return {
                'query': self._module_block['args'][0]
            }
        return None
