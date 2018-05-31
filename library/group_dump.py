#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: group_dump
short_description: Parse the group file
description:
  - Get the parsed contents of the group file.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
    - name: parse group file
      group_dump:
      register: group
    - debug:
        msg: '{{group}}'
'''

RETURN = '''
group:
    description: data structure corresponding to the fields in the group file
    returned: success
    type: list(dict)
    contains:
        group:
            description: Name of the group.
            returned: success
            type: string
            sample: users
        passwd:
            description: The old password field. Always x when shadowed passwords are used
            returned: success
            type: string
            sample: x
        gid:
            description: The group ID.
            returned: success
            type: int
            sample: 0
'''

from ansible.module_utils.basic import AnsibleModule
import re


def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    result = {'changed': False, 'group': []}

    try:
        rc, out, err = module.run_command(['cat', '/etc/group'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/group failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/group failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = line.strip()

        if line == '':
            continue
        if re.match(r'^\s*#', line):
            continue

        record = zip(('group', 'passwd', 'gid'), line.split(':'))
        record = dict(record)
        record['gid'] = int(record['gid'])
        result['group'].append(record)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
