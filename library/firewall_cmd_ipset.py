#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: firewall_cmd_ipset
short_description: Manage firewalld ipsets with firewall-cmd
description:
  - This module allows for managing aspects of firewalld direct rules.
version_added: "2.5"
author: "Casey Jaymes"
options:
    permanent:
        description:
            - Set options in permanent configuration (versus runtime configuration).
            - This option defaults to true for ansible's use case vs. the firewall-cmd default of false.
        type: bool
        default: true
    state:
        description:
            - The state expected of the option specified.
            - For entry adds or removes to be reflected in runtime, firewall_cmd state: reload will have to be issued.
        choices:
            - present
            - absent
            - enabled
            - disabled
        type: str
    name:
        description:
            - Name of the ipset
            - If the entry option is not specified, state applies to the ipset itself.
        type: str
    description:
        description:
            - Description of the ipset
            - Requires the name option
        type: str
    short:
        description:
            - Short description of the ipset
            - Requires the name option
        type: str
    family:
        description:
            - The family of the ipset
            - Requires the name option
        choices:
            - inet
            - inet6
    type:
        description:
            - The type of the ipset
            - Requires the name option
        choices:
            - hash:ip
            - hash:ip,mark
            - hash:ip,port
            - hash:ip,port,ip
            - hash:ip,port,net
            - hash:mac
            - hash:net
            - hash:net,iface
            - hash:net,net
            - hash:net,port
            - hash:net,port,net
        type: str
        default: hash:ip
    options:
        description:
            - A dict of the desired options on the ipset
            - Requires the name option
        type: dict(str, str)
        default: {}
    entry:
        description:
            - An entry in the ipset
            - Requires the name option
        type: str
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.firewall_cmd_utils import FirewallCmdAnsibleModule


def set_list_option(module, query_arg, add_arg, remove_arg, options):
    if module.params['permanent'] is not None and not module.params['permanent']:
        cmd = 'firewall-cmd'
    else:
        cmd = 'firewall-cmd --permanent'

    changed = False

    try:
        rc, out, err = module.run_command(
            ' '.join((cmd, query_arg, options)),
            use_unsafe_shell=True)
        if len(err) > 0:
            module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
        value_exists = 'yes' in out
    except OSError as exception:
        module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    if module.params['state'] in ['enabled', 'present'] and not value_exists:
        # if state will change, set changed true
        changed = True
        if not module.check_mode:
            try:
                rc, out, err = module.run_command(
                    ' '.join((cmd, add_arg, options)),
                    use_unsafe_shell=True)
                if len(err) > 0:
                    module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
            except OSError as exception:
                module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))
    elif module.params['state'] in ['disabled', 'absent'] and value_exists:
        # if state will change, set changed true
        changed = True
        if not module.check_mode:
            try:
                rc, out, err = module.run_command(
                    ' '.join((cmd, remove_arg, options)),
                    use_unsafe_shell=True)
                if len(err) > 0:
                    module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
            except OSError as exception:
                module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    return changed

def main():
    # set up the module & defaults
    module = FirewallCmdAnsibleModule(
        argument_spec=dict(
            permanent=dict(type='bool', default=True),
            state=dict(type='str', choices=['present', 'absent', 'enabled', 'disabled']),
            name=dict(type='str'),
            description=dict(type='str'),
            short=dict(type='str'),
            family=dict(type='str', choices=['inet', 'inet6'], default='inet'),
            type=dict(type='str', choices=[
                'hash:ip',
                'hash:ip,mark',
                'hash:ip,port',
                'hash:ip,port,ip',
                'hash:ip,port,net',
                'hash:mac',
                'hash:net',
                'hash:net,iface',
                'hash:net,net',
                'hash:net,port',
                'hash:net,port,net',
            ]),
            options=dict(type='dict', default={}),
            entry=dict(type='str'),
        ),
        supports_check_mode=True
    )

    if not module.firewalld_installed():
        module.fail_json(msg='firewalld is not installed')
    if not module.firewalld_running():
        module.fail_json(msg='firewalld is not running')

    result = {'changed': False}

    if module.params['permanent'] is not None and not module.params['permanent']:
        cmd = []
    else:
        cmd = ['--permanent']

    if module.params['entry'] is not None:
        if module.params['state'] is None:
            module.fail_json(msg='The state option is required with the entry option')
        if module.params['name'] is None:
            module.fail_json(msg='The name option is required with the entry option')

        if set_list_option(
            module,
            '--ipset="{0}" --query-entry'.format(module.params['name']),
            '--ipset="{0}" --add-entry'.format(module.params['name']),
            '--ipset="{0}" --remove-entry'.format(module.params['name']),
            module.params['entry']
        ):
            # if state will change, set changed true
            result['changed'] = True

    # NOTE: the following option must be processed after entry to avoid double processing
    elif module.params['state'] is not None:
        if module.params['name'] is None:
            module.fail_json(msg='The name option is required with the entry option')

        ipset_exists = None
        if module.params['name'] in module.firewall_cmd(cmd + ['--get-ipsets']).strip().split(' '):
            ipset_exists = True
        else:
            ipset_exists = False

        if module.params['state'] in ['enabled', 'present'] and not ipset_exists:
            # if state will change, set changed true
            result['changed'] = True
            if not module.check_mode:
                cmd = cmd + [
                    '--new-ipset="{0}"'.format(module.params['name']),
                    '--type={0}'.format(module.params['type']),
                    '--family={0}'.format(module.params['family']),
                    ]
                for k,v in module.params['options']:
                    if v is None:
                        cmd.append('--option=' + str(k))
                    else:
                        cmd.append('--option=' + str(k) + '=' + str(v))
                module.firewall_cmd(cmd)

        elif module.params['state'] in ['disabled', 'absent'] and ipset_exists:
            # if state will change, set changed true
            result['changed'] = True
            if not module.check_mode:
                module.firewall_cmd(cmd + ['--delete-ipset="{0}"'.format(module.params['name'])])

    if module.version_cmp('0.4.3.2', module.firewalld_version()) <= 0 and (
        module.params['state'] is None
        or module.params['state'] in ['enabled', 'present']
    ):
        if module.params['description'] is not None:
            cur_desc = module.firewall_cmd(cmd + ['--get-description']).strip()
            if cur_desc != module.params['description']:
                result['changed'] = True
                if not module.check_mode:
                    module.firewall_cmd(cmd + ['--set-description={0}'.format(module.params['description'])])
        if module.params['short'] is not None:
            cur_desc = module.firewall_cmd(cmd + ['--get-short']).strip()
            if cur_desc != module.params['short']:
                result['changed'] = True
                if not module.check_mode:
                    module.firewall_cmd(cmd + ['--set-short={0}'.format(module.params['short'])])

    module.exit_json(**result)

if __name__ == '__main__':
    main()
