#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: rsyslog_files
short_description: Parse the rsyslog config file
description:
  - Get the log files created via the rsyslog config file.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
    - name: parse rsyslog file
      rsyslog_files:
      register: rsyslog_files
    - debug:
        msg: '{{rsyslog_files}}'
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
import re


def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    result = {'changed': False, 'files': []}

    try:
        rc, out, err = module.run_command('cat /etc/rsyslog.conf /etc/rsyslog.d/*', use_unsafe_shell=True)
    except OSError as exception:
        # ignore errors from /*
        pass

    for line in out.splitlines():
        line = line.strip()
        line = line.split('#')[0]

        if line == '':
            continue

        # skip directives
        if line.startswith('$'):
            continue

        (selector, action) = line.split(None, 2)
        if action[0] in ':|@~$^' or action.startswith('/dev'):
            continue

        if action[0] == '-':
            # strip off -
            action = action[1:]

        result['files'].append(action)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
