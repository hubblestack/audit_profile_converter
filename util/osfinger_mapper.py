import json
import logging

log = logging.getLogger(__name__)

class OsfingerMapper:
    """
    A mapper class, which maps OS string to OSfinger as per mapping json
    """
    def __init__(self, static_mapping_data_folder):
        self._osfinger_map = {}
        with open(static_mapping_data_folder) as f:
            self._osfinger_map = json.load(f)

    def get(self, os):
        if os in self._osfinger_map:
            return self._osfinger_map[os]

        log.warn(f'Could not find a valid mapping for os: {os}')
        # else return as it is
        return os

    def convert_str(self, os_str):
        os_list = [x.strip() for x in os_str.split(',')]
        result = []
        for oss in os_list:
            c_oss = self.get(oss).replace(' ', '*')
            result.append(self.get(c_oss))

        return 'G@osfinger:' + ' or G@osfinger:'.join(result)