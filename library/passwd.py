#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: passwd
short_description: Parse the passwd file
description:
  - Get the parsed contents of the passwd file.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
    - name: parse passwd file
      interactive_homes:
      register: int_homes
    - debug:
        msg: '{{int_homes}}'
'''

RETURN = '''
home_directories:
    description: data structure corresponding to the fields in the passwd file
    returned: success
    type: list(dict)
    contains:
        login:
            description: Login of the user.
            returned: success
            type: string
            sample: root
        passwd:
            description: The old password field. Always x when shadowed passwords are used
            returned: success
            type: string
            sample: x
        uid:
            description: The ID of the user.
            returned: success
            type: int
            sample: 0
        gid:
            description: The primary group ID of the user.
            returned: success
            type: int
            sample: 0
        name:
            description: Comment field. Usually the user's full name.
            returned: success
            type: string
            sample: Root User
        home:
            description: The home directory of the user.
            returned: success
            type: string
            sample: /root
        shell:
            description: The shell spawned for the user. /sbin/nologin can be used for users not able to log in.
            returned: success
            type: string
            sample: /bin/bash
'''

from ansible.module_utils.basic import AnsibleModule
import re


def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    result = {'changed': False, 'home_directories': []}

    try:
        rc, out, err = module.run_command(['cat', '/etc/passwd'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/passwd failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/passwd failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        record = zip(('login', 'passwd', 'uid', 'gid', 'name', 'home', 'shell'), line.strip().split(':'))
        record = dict(record)
        record['uid'] = int(record['uid'])
        record['gid'] = int(record['gid'])
        result['home_directories'].append(record)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
