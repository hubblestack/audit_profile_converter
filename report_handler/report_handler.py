import os
import logging
import yaml

# for html templates (mustache lib)
import chevron

from util import helper

log = logging.getLogger(__name__)

class ReportHandler:
    def __init__(self, folder, profile_folder, profile_filepath, template_folder):
        self._folder = folder
        self._report_file = profile_filepath.split(profile_folder)[1]
        if self._report_file.startswith('/'):
            self._report_file = self._report_file[1:]
        self._template_folder = template_folder
        self._whitelist = []
        self._blacklist = []
        self._skipped = []
        self._unhandled_count = 0

    def write(self, is_whitelist, old_data, new_data):
        if is_whitelist:
            self._whitelist.append({
                'old': self._dump_yaml(old_data),
                'new': self._dump_yaml(new_data)
            })
        else:
            self._blacklist.append({
                'old': self._dump_yaml(old_data),
                'new': self._dump_yaml(new_data)
            })
    def skipped(self, old_data):
        self._skipped.append(self._dump_yaml(old_data))

    def add_unhandled(self):
        self._unhandled_count += 1

    def _dump_yaml(self, data):
        return yaml.dump(data, sort_keys=False)

    def save(self):
        html_template = helper.read_file(self._template_folder + '/report.mustache')

        args = {
            'template': html_template,
            'partials_path': 'template/',
            'data': {
                'total': len(self._whitelist) + len(self._blacklist) + len(self._skipped),
                'unhandled_count': self._unhandled_count,
                'whitelist': {
                    'items': self._whitelist,
                    'total': len(self._whitelist),
                    'title': 'Whitelist blocks'
                },
                'blacklist': {
                    'items': self._blacklist,
                    'total': len(self._blacklist),
                    'title': 'Blacklist blocks'
                },
                'skipped': {
                    'items': self._skipped,
                    'total': len(self._skipped),
                    'title': 'Skipped blocks'
                }
            }
        }
        full_html = chevron.render(**args)
        self._write(full_html)

    def _write(self, content):
        filepath = self._folder + '/' + self._report_file + '.html'
        log.info('Writing report at: {0}'.format(filepath))
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, "w") as f:
            f.write(content)
