#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: semanage_login
short_description: Manage SELinux user contexts
description:
  - Manage SELinux user contexts.
  - Requires policycoreutils-python be installed.
version_added: "2.5"
author: "Casey Jaymes"
options:
    login:
        description:
            - Specifies the system user.
            - You can specify groups by prefixing a % .
            - Required.
        type: str
        default: None
    state:
        description:
            - The state expected of the option specified.
            - Required
        choices:
            - present
            - absent
            - enabled
            - disabled
        type: str
    seuser:
        description:
            - Specifies the SELinux user.
            - Required if state is present
        type: str
    range:
        description:
            - Specifies the SELinux MLS/MCS Security Range (MLS/MCS systems only).
        type: str
        default: s0
    store:
        description:
            - Specifies an alternate SELinux store.
        type: str
        default: None
'''

EXAMPLES = '''
'''

RETURN = '''
semanage_login:
    description:
        - Data structure corresponding to the fields in the semanage login -l command
        - The keys are the user logins
    returned: success
    type: dict(str, dict)
    contains:
        seuser:
            description: The SELinux user.
            returned: success
            type: str
            sample: user_u
        range:
            description: The MLS/MCS Security Range (on MLS/MCS systems only).
            returned: success
            type: str
            sample: s0
        service:
            description: The service.
            returned: success
            type: str
            sample: *
'''

from ansible.module_utils.basic import AnsibleModule
import re

def get_list(module):
    cmd = ['semanage', 'login']

    if module.params['store'] is not None:
        cmd.append('--store')
        cmd.append(module.params['store'])

    try:
        rc, out, err = module.run_command(cmd)
        if len(err) > 0:
            module.fail_json(msg='{0} failed with error: {1}'.format(cmd.join(' '), str(err)))
    except OSError as exception:
        module.fail_json(msg='{0} failed with exception: {1}'.format(cmd.join(' '), exception))

    l = {}
    # skip first line
    lines = out.splitlines()[1:]
    for line in lines:
        (login, seuser, range, service) = re.split(r'\s+', line.strip(), maxsplits=4)
        record = {
            'seuser': seuser,
            'range': range,
            'service': service,
        }
        l[login] = record
    return l

def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(
            login=dict(type='str'),
            state=dict(type='str', choices=['present', 'absent', 'enabled', 'disabled']),
            seuser=dict(type='str'),
            range=dict(type='str', default='s0'),
            store=dict(type='str', default=None),
        ),
        supports_check_mode=True
    )

    if module.params['login'] is None:
        module.fail_json(msg='The login option is required')
    if module.params['state'] is None:
        module.fail_json(msg='The state option is required')

    result = {'changed': False, 'semanage_login': []}

    result['semanage_login'] = get_list(module)

    cmd = ['semanage', 'login']

    if module.params['store'] is not None:
        cmd.append('--store')
        cmd.append(module.params['store'])

    if module.params['state'] in ('present', 'enabled'):
        if module.params['seuser'] is None:
            module.fail_json(msg='The seuser option is required when state is present/enabled')

        if module.params['login'] in result['semanage_login']:
            # present, but we need to check params
            record = result['semanage_login'][module.params['login']]
            if (
                record['seuser'] != module.params['seuser']
                or record['range'] != module.params['range']
            ):
                # present, modify
                result['changed'] = True
                cmd.append('--modify')
                cmd.append('--seuser')
                cmd.append(module.params['seuser'])
                cmd.append('--range')
                cmd.append(module.params['range'])
                cmd.append(module.params['login'])
        else:
            # not present, add
            result['changed'] = True
            cmd.append('--add')
            cmd.append('--seuser')
            cmd.append(module.params['seuser'])
            cmd.append('--range')
            cmd.append(module.params['range'])
            cmd.append(module.params['login'])

    elif module.params['state'] in ('absent', 'disabled'):
        if module.params['login'] in result['semanage_login']:
            result['changed'] = True
            cmd.append('--delete')
            cmd.append(module.params['login'])

    else:
        module.fail_json(msg='Unknown state option')

    if result['changed'] and not module.check_mode:
        try:
            rc, out, err = module.run_command(cmd)
            if len(err) > 0:
                module.fail_json(msg='{0} failed with error: {1}'.format(cmd.join(' '), str(err)))
        except OSError as exception:
            module.fail_json(msg='{0} failed with exception: {1}'.format(cmd.join(' '), exception))

        result['semanage_login'] = get_list(module)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
