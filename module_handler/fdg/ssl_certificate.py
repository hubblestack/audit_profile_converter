from module_handler.fdg_module_handler import FdgModuleHandler

class SSLCertificate(FdgModuleHandler):
    """
    SSLCertificate specific conversion steps
    """
    def __init__(self, report_handler, block_id, module_name, function_name, module_block):
        super().__init__(report_handler, block_id, module_name, function_name, module_block)

    def _prepare_args(self):
        """
        Prepare SSLCertificate arguments

        Example input for better understanding
            fetch_certificate_details:
                module: ssl_certificate.get_cert_details
                args:
                  - params:
                      ssl_timeout: 3
        """
        if self._function_name == 'get_cert_details':
            return self._get_cert_details()
        return None

    def _get_cert_details(self):
        return {
            'ssl_timeout': self._module_block['args'][0]['params']['ssl_timeout']
        }