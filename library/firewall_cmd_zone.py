#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: firewall_cmd_zone
short_description: Manage a zone with firewall-cmd
description:
  - This module allows for addition or deletion of zones in either running or permanent firewalld rules.
version_added: "2.5"
author: "Casey Jaymes"
options:
    name:
        description:
            - The zone to add/remove to/from.
        default: system-default(public)
        type: str
    permanent:
        description:
            - Set options in permanent configuration (versus runtime configuration).
            - This option defaults to true for ansible's use case vs. the firewall-cmd default of false.
        type: bool
        default: true
    state:
        description:
            - If only name is specified, this will add or remove the zone itself; permanent is implied.
            - For zone adds or removes to be reflected in runtime, firewall_cmd state: reload will have to be issued.
            - The state expected of the option specified.
        choices:
            - present
            - absent
            - enabled
            - disabled
        type: str
    timeout:
        description:
            - The length of time this configuration should apply before being removed.
            - Either a number (of seconds) or number followed by one of characters s (seconds), m (minutes), h (hours), for example 20m or 1h.
        type: str
    target:
        description:
            - Set the zone target.
        type: str
        choices:
            - default
            - ACCEPT
            - DROP
            - REJECT
    description:
        description:
            - Set the zone description.
            - Only usable on firewalld > 0.4.3.2
        type: str
    short:
        description:
            - Set the zone short description.
            - Only usable on firewalld > 0.4.3.2
        type: str
    icmp_block_inversion:
        description:
            - Set the icmp-block-inversion for this zone.
        type: bool
    interface:
        description:
            - The interface to relate to the zone.
            - NOTE: this currently doesn't work if ZONE is specified in /etc/sysconfig/network-scripts/ifcfg-*
            - The state option should be used to specify if the interface is present or absent.
        type: str
    source:
        description:
            - The source to relate to the zone.
            - The state option should be used to specify if the source is present or absent.
        type: str
    service:
        description:
            - The service to relate to the zone (from firewall-cmd --get-services).
            - The state option should be used to specify if the service is present or absent.
            - The timeout option can be used with this option.
        type: str
    port:
        description:
            - The port to relate to the zone: portid[-portid]/protocol
            - The state option should be used to specify if the port is present or absent.
            - The timeout option can be used with this option.
        type: str
    protocol:
        description:
            - The protocol to relate to the zone (from /etc/protocols).
            - The state option should be used to specify if the protocol is present or absent.
            - The timeout option can be used with this option.
        type: str
    masquerade:
        description:
            - Set masquerading for this zone.
            - The timeout option can be used with this option.
        type: bool
    forward_port:
        description:
            - The forward_port to relate to the zone: port=portid[-portid]:proto=protocol[:toport=portid[-portid]][:toaddr=address]
            - NOTE: specifying the /mask results in an error from firewall-cmd, though it's in the man page.
            - The port can either be a single port number portid or a port range portid-portid.
            - The protocol can either be tcp, udp, sctp or dccp. The destination address is a simple IP address.
            - The state option should be used to specify if the forward_port is present or absent.
            - The timeout option can be used with this option.
        type: str
    source_port:
        description:
            - The source_port to relate to the zone: portid[-portid]/protocol
            - The state option should be used to specify if the source_port is present or absent.
            - The timeout option can be used with this option.
        type: str
    icmp_block:
        description:
            - The icmp_block to relate to the zone: icmptype (from firewall-cmd --get-icmptypes)
            - The state option should be used to specify if the icmp_block is present or absent.
            - The timeout option can be used with this option.
        type: str
    rich_rule:
        description:
            - The rich_rule to relate to the zone (from firewalld.richlanguage(5)).
            - The state option should be used to specify if the rich_rule is present or absent.
            - The timeout option can be used with this option.
        type: str
'''

EXAMPLES = '''
    - name: create zone; permanent is implied
      firewall_cmd_zone:
        name: test
        state: present

    - name: reload permanent configuration into runtime (necessary after zone creation)
      firewall_cmd:
        state: reload

    - name: set zone description; permanent is implied
      firewall_cmd_zone:
        name: test
        description: Long description of a zone for testing

    - name: set zone short description; permanent is implied
      firewall_cmd_zone:
        name: test
        short: Zone for testing

    - name: set zone target; permanent is implied
      firewall_cmd_zone:
        name: test
        target: ACCEPT

    # - name: add an interface to a zone
    #   firewall_cmd_zone:
    #     name: test
    #     interface: eth0
    #     state: present
    # - name: remove an interface from a zone
    #   firewall_cmd_zone:
    #     name: test
    #     interface: eth0
    #     state: absent

    - name: set zone icmp block inversion
      firewall_cmd_zone:
        name: test
        icmp_block_inversion: true
    - name: reset zone icmp block inversion
      firewall_cmd_zone:
        name: test
        icmp_block_inversion: false

    - name: add a source to a zone
      firewall_cmd_zone:
        name: test
        source: 192.168.0.0/16
        state: present
    - name: remove a source from a zone
      firewall_cmd_zone:
        name: test
        source: 192.168.0.0/16
        state: absent

    - name: add a service to a zone
      firewall_cmd_zone:
        name: test
        service: ssh
        state: present
    - name: remove a service from a zone
      firewall_cmd_zone:
        name: test
        service: ssh
        state: absent

    - name: add a port to a zone
      firewall_cmd_zone:
        name: test
        port: 22/tcp
        state: present
    - name: remove a port from a zone
      firewall_cmd_zone:
        name: test
        port: 22/tcp
        state: absent

    - name: add a protocol to a zone
      firewall_cmd_zone:
        name: test
        protocol: gre
        state: present
    - name: remove a protocol from a zone
      firewall_cmd_zone:
        name: test
        protocol: gre
        state: absent

    - name: set zone masquerading
      firewall_cmd_zone:
        name: test
        masquerade: true
    - name: reset zone masquerading
      firewall_cmd_zone:
        name: test
        masquerade: false

    - name: add a forward-port to a zone
      firewall_cmd_zone:
        name: test
        forward_port: port=3389:proto=tcp:toport=3389:toaddr=192.168.42.42
        state: present
    - name: remove a forward-port from a zone
      firewall_cmd_zone:
        name: test
        forward_port: port=3389:proto=tcp:toport=3389:toaddr=192.168.42.42
        state: absent

    - name: add a source-port to a zone
      firewall_cmd_zone:
        name: test
        source_port: 68/udp
        state: present
    - name: remove a source-port from a zone
      firewall_cmd_zone:
        name: test
        source_port: 68/udp
        state: absent

    - name: add an icmp-block to a zone
      firewall_cmd_zone:
        name: test
        icmp_block: echo-request
        state: present
    - name: remove an icmp-block from a zone
      firewall_cmd_zone:
        name: test
        icmp_block: echo-request
        state: absent

    - name: add a rich rule to a zone
      firewall_cmd_zone:
        name: test
        rich_rule: rule protocol value="ah" accept
        state: present
    - name: remove a rich rule from a zone
      firewall_cmd_zone:
        name: test
        rich_rule: rule protocol value="ah" accept
        state: absent

    - name: delete zone; permanent is implied
      firewall_cmd_zone:
        name: test
        state: absent

    - name: reload permanent configuration into runtime (necessary after zone deletion)
      firewall_cmd:
        state: reload
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.firewall_cmd_utils import FirewallCmdAnsibleModule


def set_zone_bool_option(module, query_arg, add_arg, remove_arg, option):
    if module.params['permanent'] is not None and not module.params['permanent']:
        cmd = 'firewall-cmd'
    else:
        cmd = 'firewall-cmd --permanent'

    if module.params['name'] is not None:
        cmd += ' --zone=' + module.params['name']

    changed = False

    try:
        rc, out, err = module.run_command(
            "{0} {1}".format(cmd, query_arg),
            use_unsafe_shell=True)
        if len(err) > 0:
            module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
        value = out.strip()
        if value == 'yes':
            value = True
        else:
            value = False
    except OSError as exception:
        module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    if value != option:
        # if state will change, set changed true
        changed = True
        if not module.check_mode:
            if option:
                try:
                    rc, out, err = module.run_command(
                        "{0} {1}".format(cmd, add_arg),
                        use_unsafe_shell=True)
                    if len(err) > 0:
                        module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
                except OSError as exception:
                    module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))
            else:
                try:
                    rc, out, err = module.run_command(
                        "{0} {1}".format(cmd, remove_arg),
                        use_unsafe_shell=True)
                    if len(err) > 0:
                        module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
                except OSError as exception:
                    module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    return changed

def set_zone_option(module, query_arg, set_arg, option):
    if module.params['permanent'] is not None and not module.params['permanent']:
        cmd = 'firewall-cmd'
    else:
        cmd = 'firewall-cmd --permanent'

    if module.params['name'] is not None:
        cmd += ' --zone=' + module.params['name']

    changed = False

    try:
        rc, out, err = module.run_command(
            "{0} {1}".format(cmd, query_arg),
            use_unsafe_shell=True)
        if len(err) > 0:
            module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
        value = out.strip()
    except OSError as exception:
        module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    if option != value:
        # if state will change, set changed true
        changed = True
        if not module.check_mode:
            try:
                rc, out, err = module.run_command(
                    "{0} {1}='{2}'".format(cmd, set_arg, option),
                    use_unsafe_shell=True)
                if len(err) > 0:
                    module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
            except OSError as exception:
                module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    return changed

def set_perm_zone_option(module, query_arg, set_arg, option):
    cmd = 'firewall-cmd --permanent'

    if module.params['name'] is not None:
        cmd += ' --zone=' + module.params['name']

    changed = False

    try:
        rc, out, err = module.run_command(
            "{0} {1}".format(cmd, query_arg),
            use_unsafe_shell=True)
        if len(err) > 0:
            module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
        value = out.strip()
    except OSError as exception:
        module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    if option != value:
        # if state will change, set changed true
        changed = True
        if not module.check_mode:
            try:
                rc, out, err = module.run_command(
                    "{0} {1}='{2}'".format(cmd, set_arg, option),
                    use_unsafe_shell=True)
                if len(err) > 0:
                    module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
            except OSError as exception:
                module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    return changed

def set_zone_list_option(module, query_arg, add_arg, remove_arg, option):
    if module.params['state'] is None:
        module.fail_json(msg='The state option is required')

    if module.params['permanent'] is not None and not module.params['permanent']:
        cmd = 'firewall-cmd'
    else:
        cmd = 'firewall-cmd --permanent'

    if module.params['name'] is not None:
        cmd += ' --zone=' + module.params['name']

    if module.params['timeout'] is not None:
        timeout = ' --timeout=' + module.params['timeout']
    else:
        timeout = ''

    changed = False

    try:
        rc, out, err = module.run_command(
            "{0} {1}='{2}'".format(cmd, query_arg, option),
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
                    "{0} {1}='{2}'{3}".format(cmd, add_arg, option, timeout),
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
                    "{0} {1}='{2}'{3}".format(cmd, remove_arg, option, timeout),
                    use_unsafe_shell=True)
                if len(err) > 0:
                    module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
            except OSError as exception:
                module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

    return changed

def set_zone_interface(module):
    if module.params['state'] is None:
        module.fail_json(msg='The state option is required with the interface option')

    changed = False

    # check nmcli first
    nmcli_managed = True
    try:
        rc, out, err = module.run_command(
            "nmcli con show {0} | grep '^connection\.zone'".format(module.params['interface']),
            use_unsafe_shell=True)
        if len(err) > 0:
            nmcli_managed = False
    except OSError as exception:
        nmcli_managed = False
    if nmcli_managed:
        cur_zone = out.split(':')[1].strip()

        if module.params['state'] in ['enabled', 'present'] and cur_zone != module.params['name']:
            changed = True
            if not module.check_mode:
                try:
                    rc, out, err = module.run_command(
                        "nmcli con modify {0} connection.zone {1}".format(module.params['interface'], module.params['name']),
                        use_unsafe_shell=True)
                    if len(err) > 0:
                        module.fail_json(msg='nmcli con modify failed with error: {0}'.format(str(err)))
                except OSError as exception:
                    module.fail_json(msg='nmcli con modify failed with exception: {0}'.format(exception))
        elif module.params['state'] in ['disabled', 'absent'] and cur_zone == module.params['name']:
            changed = True
            if not module.check_mode:
                try:
                    # This just moves the con back to the default zone; close as we can get to "removing"
                    rc, out, err = module.run_command(
                        "nmcli con modify {0} connection.zone NULL".format(module.params['interface']),
                        use_unsafe_shell=True)
                    if len(err) > 0:
                        module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
                except OSError as exception:
                    module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

        if changed and not module.check_mode:
            try:
                rc, out, err = module.run_command("systemctl restart network".split(' '))
                if len(err) > 0:
                    module.fail_json(msg='systemctl restart network failed with error: {0}'.format(str(err)))
            except OSError as exception:
                module.fail_json(msg='systemctl restart network failed with exception: {0}'.format(exception))
    else:
        if module.params['permanent'] is not None and not module.params['permanent']:
            cmd = 'firewall-cmd'
        else:
            cmd = 'firewall-cmd --permanent'

        if module.params['name'] is not None:
            cmd += ' --zone=' + module.params['name']

        if module.params['timeout'] is not None:
            timeout = ' --timeout=' + module.params['timeout']
        else:
            timeout = ''

        try:
            rc, out, err = module.run_command(
                "{0} --query-interface='{1}'".format(cmd, module.params['interface']),
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
                        "{0} --add-interface='{1}'{2}".format(cmd, module.params['interface'], timeout),
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
                        "{0} --remove-interface='{1}'{2}".format(cmd, module.params['interface'], timeout),
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
            name=dict(type='str'),
            permanent=dict(type='bool', default=True),
            state=dict(type='str', choices=['present', 'absent', 'enabled', 'disabled', 'reload']),
            timeout=dict(type='str'),
            description=dict(type='str'),
            short=dict(type='str'),
            target=dict(type='str', choices=['default', 'ACCEPT', 'DROP', 'REJECT']),
            icmp_block_inversion=dict(type='bool'),
            interface=dict(type='str'),
            source=dict(type='str'),
            service=dict(type='str'),
            port=dict(type='str'),
            protocol=dict(type='str'),
            masquerade=dict(type='bool'),
            forward_port=dict(type='str'),
            source_port=dict(type='str'),
            icmp_block=dict(type='str'),
            rich_rule=dict(type='str'),
        ),
        supports_check_mode=True
    )

    if not module.firewalld_installed():
        module.fail_json(msg='firewalld is not installed')
    if not module.firewalld_running():
        module.fail_json(msg='firewalld is not running')

    result = {'changed': False}

    if (
        module.params['permanent'] is not None and module.params['permanent']
        and module.params['timeout'] is not None
    ):
        module.fail_json(msg='permanent and timeout options cannot be used together')

    # TODO --new-zone-from-file
    # TODO --load-zone-defaults

    options = [
        'description',
        'short',
        'target',
        'icmp_block_inversion',
        'interface',
        'source',
        'service',
        'port',
        'protocol',
        'masquerade',
        'forward_port',
        'source_port',
        'icmp_block',
        'rich_rule',
    ]
    options_none = [module.params[k] is None for k in options]

    # if all the options are None, we want to create/remove the zone
    if all(options_none):
        if module.params['name'] is None:
            module.fail_json(msg='The name option is required to create or remove a zone')
        if module.params['state'] is None:
            module.fail_json(msg='The state option is required to create or remove a zone')

        # check if zone exists
        try:
            rc, out, err = module.run_command(
                "firewall-cmd --permanent --get-zones",
                use_unsafe_shell=True)
            if len(err) > 0:
                module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
        except OSError as exception:
            module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))
        zone_exists = module.params['name'] in out.strip().split()

        # apply changes if needed
        if module.params['state'] in ['enabled', 'present'] and not zone_exists:
            result['changed'] = True
            if not module.check_mode:
                try:
                    rc, out, err = module.run_command(
                        "firewall-cmd --permanent --new-zone={0}".format(module.params['name']),
                        use_unsafe_shell=True)
                    if len(err) > 0:
                        module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
                except OSError as exception:
                    module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))
        elif module.params['state'] in ['disabled', 'absent'] and zone_exists:
            result['changed'] = True
            if not module.check_mode:
                try:
                    rc, out, err = module.run_command(
                        "firewall-cmd --permanent --delete-zone={0}".format(module.params['name']),
                        use_unsafe_shell=True)
                    if len(err) > 0:
                        module.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
                except OSError as exception:
                    module.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))

        module.exit_json(**result)

    if (
        module.version_cmp('0.4.3.2', module.firewalld_version()) <= 0
        and module.params['description'] is not None
    ):
        module.fail_json(msg='The "description" feature is not available in firewalld ' + module.firewalld_version())
    elif module.params['description'] is not None and set_perm_zone_option(
        module,
        '--get-description',
        '--set-description',
        module.params['description']
    ):
        # if state will change, set changed true
        result['changed'] = True

    if (
        module.version_cmp('0.4.3.2', module.firewalld_version()) <= 0
        and module.params['short'] is not None
    ):
        module.fail_json(msg='The "short" feature is not available in firewalld ' + module.firewalld_version())
    elif module.params['short'] is not None and set_perm_zone_option(
        module,
        '--get-short',
        '--set-short',
        module.params['short']
    ):
        # if state will change, set changed true
        result['changed'] = True

    if module.params['target'] is not None and set_perm_zone_option(
        module,
        '--get-target',
        '--set-target',
        module.params['target']
    ):
        # if state will change, set changed true
        result['changed'] = True

    if module.params['icmp_block_inversion'] is not None and set_zone_bool_option(
        module,
        '--query-icmp-block-inversion',
        '--add-icmp-block-inversion',
        '--remove-icmp-block-inversion',
        module.params['icmp_block_inversion']
    ):
        result['changed'] = True

    if module.params['masquerade'] is not None and set_zone_bool_option(
        module,
        '--query-masquerade',
        '--add-masquerade',
        '--remove-masquerade',
        module.params['masquerade']
    ):
        result['changed'] = True

    if module.params['interface'] is not None and set_zone_interface(module):
        result['changed'] = True

    if module.params['source'] is not None and set_zone_list_option(
        module,
        '--query-source',
        '--add-source',
        '--remove-source',
        module.params['source']
    ):
        result['changed'] = True

    if module.params['service'] is not None and set_zone_list_option(
        module,
        '--query-service',
        '--add-service',
        '--remove-service',
        module.params['service']
    ):
        result['changed'] = True

    if module.params['port'] is not None and set_zone_list_option(
        module,
        '--query-port',
        '--add-port',
        '--remove-port',
        module.params['port']
    ):
        result['changed'] = True

    if module.params['protocol'] is not None and set_zone_list_option(
        module,
        '--query-protocol',
        '--add-protocol',
        '--remove-protocol',
        module.params['protocol']
    ):
        result['changed'] = True

    if module.params['forward_port'] is not None and set_zone_list_option(
        module,
        '--query-forward-port',
        '--add-forward-port',
        '--remove-forward-port',
        module.params['forward_port']
    ):
        result['changed'] = True

    if module.params['source_port'] is not None and set_zone_list_option(
        module,
        '--query-source-port',
        '--add-source-port',
        '--remove-source-port',
        module.params['source_port']
    ):
        result['changed'] = True

    if module.params['icmp_block'] is not None and set_zone_list_option(
        module,
        '--query-icmp-block',
        '--add-icmp-block',
        '--remove-icmp-block',
        module.params['icmp_block']
    ):
        result['changed'] = True

    if module.params['rich_rule'] is not None and set_zone_list_option(
        module,
        '--query-rich-rule',
        '--add-rich-rule',
        '--remove-rich-rule',
        module.params['rich_rule']
    ):
        result['changed'] = True

    # report back the results
    module.exit_json(**result)

if __name__ == '__main__':
    main()
