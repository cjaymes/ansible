#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: firewall_cmd_direct
short_description: Manage firewalld direct rules with firewall-cmd
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
            - For direct adds or removes to be reflected in runtime, firewall_cmd state: reload will have to be issued.
            - The state expected of the option specified.
        choices:
            - present
            - absent
            - enabled
            - disabled
        type: str
    family:
        description:
            - The network firewall family to modify
        choices:
            - ipv4
            - ipv6
            - eb
        type: str
        default: ipv4
    table:
        description:
            - Specifies the table to modify
        type: str
    chain:
        description:
            - Specifies the chain to add/remove/modify.
            - Requires the table and state options.
        type: str
    priority:
        description:
            - The priority is used to order rules.
            - Priority 0 means add rule on top of the chain, with a higher priority the rule will be added further down.
            - Rules with the same priority are on the same level and the order of these rules is not fixed and may change.
            - If you want to make sure that a rule will be added after another one, use a low priority for the first and a higher for the following.
        type: int
        default: 0
    rule:
        description:
            - Adds or removes a rule within the specified family, table and chain.
            - Requires the state, family (defaults to ipv4), table and chain options
        type: str
    passthrough:
        description:
            - Adds or removes a passthrough within the specified table.
            - Requires the state and family (defaults to ipv4) options
        type: str
'''

EXAMPLES = '''
    - name: add a direct chain
      firewall_cmd_direct:
        family: ipv4
        table: filter
        chain: IN_test_allow
        state: present
    - name: remove a direct chain
      firewall_cmd_direct:
        family: ipv4
        table: filter
        chain: IN_test_allow
        state: absent

    - name: add a direct rule
      firewall_cmd_direct:
        family: ipv4
        table: filter
        chain: IN_test_allow
        priority: 0
        rule: -m tcp -p tcp -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
        state: present
    - name: remove a direct rule
      firewall_cmd_direct:
        family: ipv4
        table: filter
        chain: IN_test_allow
        priority: 0
        rule: -m tcp -p tcp -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
        state: absent

    - name: add a direct passthrough
      firewall_cmd_direct:
        family: ipv4
        passthrough: -A IN_test_allow -p tcp -m tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT
        state: present
    - name: remove a direct passthrough
      firewall_cmd_direct:
        family: ipv4
        passthrough: -A IN_test_allow -p tcp -m tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT
        state: absent
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
            family=dict(type='str', choices=['ipv4', 'ipv6', 'eb'], default='ipv4'),
            table=dict(type='str'),
            chain=dict(type='str'),
            priority=dict(type='int', default=0),
            rule=dict(type='str'),
            passthrough=dict(type='str')
        ),
        supports_check_mode=True
    )

    if not module.firewalld_installed():
        module.fail_json(msg='firewalld is not installed')
    if not module.firewalld_running():
        module.fail_json(msg='firewalld is not running')

    result = {'changed': False}

    if module.params['rule'] is not None:
        if module.params['state'] is None:
            module.fail_json(msg='The state option is required with the rule option')
        # NOTE: family is always defined; default or explicit
        if module.params['table'] is None:
            module.fail_json(msg='The table option is required with the rule option')
        if module.params['chain'] is None:
            module.fail_json(msg='The chain option is required with the rule option')
        # NOTE: priority is always defined

        options = ' '.join((
            module.params['family'],
            module.params['table'],
            module.params['chain'],
            str(module.params['priority']),
            module.params['rule']
        ))
        if set_list_option(
            module,
            '--direct --query-rule',
            '--direct --add-rule',
            '--direct --remove-rule',
            options
        ):
            # if state will change, set changed true
            result['changed'] = True

    # NOTE: this option must be processed after rule to avoid processing rules as chain
    if module.params['chain'] is not None:
        if module.params['state'] is None:
            module.fail_json(msg='The state option is required with the chain option')
        # NOTE: family is always defined; default or explicit
        if module.params['table'] is None:
            module.fail_json(msg='The table option is required with the chain option')

        options = ' '.join((
            module.params['family'],
            module.params['table'],
            module.params['chain'],
        ))
        if set_list_option(
            module,
            '--direct --query-chain',
            '--direct --add-chain',
            '--direct --remove-chain',
            options
        ):
            # if state will change, set changed true
            result['changed'] = True

    if module.params['passthrough'] is not None:
        if module.params['state'] is None:
            module.fail_json(msg='The state option is required with the passthrough option')
        # NOTE: family is always defined; default or explicit

        options = ' '.join((
            module.params['family'],
            module.params['passthrough'],
        ))
        if set_list_option(
            module,
            '--direct --query-passthrough',
            '--direct --add-passthrough',
            '--direct --remove-passthrough',
            options
        ):
            # if state will change, set changed true
            result['changed'] = True

    module.exit_json(**result)

if __name__ == '__main__':
    main()
