#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: shadow
short_description: Parse the shadow file
description:
  - Get the parsed contents of the shadow file.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
    - name: parse shadow file
      register: shadow
    - debug:
        msg: '{{shadow}}'
'''

RETURN = '''
shadow:
    description: data structure corresponding to the fields in the shadow file
    returned: success
    type: list(dict)
    contains:
        login:
            description: Login of the user.
            returned: success
            type: str
            sample: root
        no_passwd:
            description: True when no password is required to login ('')
            returned: success
            type: bool
            sample: False
        disabled:
            description: True when account is disabled (*)
            returned: success
            type: bool
            sample: False
        locked:
            description: True when password is locked (starts with !)
            returned: success
            type: bool
            sample: False
        lastchg:
            description: The number of days (since January 1, 1970) since the password was last changed.
            returned: success
            type: int
            sample: 12825
        mindays:
            description: The number of days before password may be changed (0 indicates it may be changed at any time)
            returned: success
            type: int
            sample: 0
        maxdays:
            description: The number of days after which password must be changed (99999 indicates user can keep his or her password unchanged for many, many years).
            returned: success
            type: int
            sample: 90
        warndays:
            description: The number of days to warn user of an expiring password (7 for a full week)
            returned: success
            type: int
            sample: 5
        inactive:
            description: The number of days after password expires that account is disabled
            returned: success
            type: int
            sample: 30
        expire:
            description: The number of days since January 1, 1970 that an account has been disabled
            returned: success
            type: int
            sample: 13096
        reserved:
            description: A reserved field for possible future use
            returned: success
            type: str
            sample:
'''

from ansible.module_utils.basic import AnsibleModule
import re


def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    result = {'changed': False, 'shadow': []}

    try:
        rc, out, err = module.run_command(['cat', '/etc/shadow'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/shadow failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/shadow failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = line.strip()
        if line == '':
            continue
        if re.match(r'^\s*#', line):
            continue
        record = zip(('login', 'passwd', 'lastchg', 'mindays', 'maxdays', 'warndays', 'inactive', 'expire', 'reserved'), line.split(':'))
        record = dict(record)

        record['no_passwd'] = record['passwd'] == ''
        record['disabled'] = record['passwd'] == '*'
        record['locked'] = record['passwd'].startswith('!')
        del record['passwd']

        for k in ('lastchg', 'mindays', 'maxdays', 'warndays', 'inactive', 'expire'):
            if record[k] == '':
                record[k] = None
            else:
                record[k] = int(record[k])
        result['shadow'].append(record)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
