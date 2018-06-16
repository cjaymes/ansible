#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: login_defs_dump
short_description: Parse the login.defs file
description:
  - Get the parsed contents of the login.defs file.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
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

    result = {'changed': False, 'login_defs': {}}

    try:
        rc, out, err = module.run_command(['cat', '/etc/login.defs'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/login.defs failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/login.defs failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = re.sub(r'^(.*)#.*$', '\\1', line)
        line = line.strip()
        if line == '':
            continue

        print(line)
        key, value = line.split(None, 1)
        result['login_defs'][key] = value

    module.exit_json(**result)

if __name__ == '__main__':
    main()
