class MiscPkg1:
    """
    Misc custom handling (for functions we did not implement)
    """
    def __init__(self, report_handler, yaml_block):
        self._report_handler = report_handler
        self._yaml_block = yaml_block

    def convert(self):
        result = []
        pkgs = self._yaml_block['args'][0].split(',')
        for pkg in pkgs:
            single_pkg = {
                'args': {'name': pkg.strip()},
                'comparator': {
                    'type': 'dict',
                    'match_key_any': [pkg.strip()]
                }
            }
            result.append(single_pkg)
        return result
    