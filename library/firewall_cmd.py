#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: firewall_cmd
short_description: Manage firewalld with firewall-cmd
description:
  - This module allows for managing aspects of firewalld itself.
version_added: "2.5"
author: "Casey Jaymes"
options:
    default_zone:
        description:
            - The zone to set as the system default zone.
        type: str
    state:
        description:
            - If the state is reload, reload firewall rules and keep state information. Current permanent configuration will become new runtime configuration, i.e. all runtime only changes done until reload are lost with reload if they have not been also in permanent configuration.
            - If the state is complete-reload, reload firewall completely, even netfilter kernel modules. This will most likely terminate active connections, because state information is lost. This option should only be used in case of severe firewall problems. For example if there are state information problems that no connection can be established with correct firewall rules.
            - If the state is save, the runtime configuration is saved into permanent.
            - If the state is get, the firewall configuration is returned.
            - If the state is get_version, the firewall version and status is returned.
        choices:
            - reload
            - complete-reload
            - save
            - get
            - get_version
        type: str
    log_denied:
        description:
            - Add logging rules right before reject and drop rules in the INPUT, FORWARD and OUTPUT chains for the default rules and also final reject and drop rules in zones for the configured link-layer packet type.
            - This is a runtime and permanent change and will also reload the firewall to be able to add the logging rules.
        default: off
        choices:
            - all
            - unicast
            - broadcast
            - multicast
            - off
    automatic_helpers:
        description:
            - For the secure use of iptables and connection tracking helpers it is recommended to turn AutomaticHelpers off.
            - But this might have side effects on other services using the netfilter helpers as the sysctl setting in /proc/sys/net/netfilter/nf_conntrack_helper will be changed.
            - With the system setting, the default value set in the kernel or with sysctl will be used.
            - This is a runtime and permanent change and will also reload the firewall to be able to add the logging rules.
            - Only usable on firewalld > 0.4.3.2
        default: system
        choices:
            - yes
            - no
            - system
'''

EXAMPLES = '''
    - name: get firewall configuration
      firewall_cmd:
          state: get
      register: firewalld_config
    - debug:
        msg: '{{firewalld_config}}'

    - name: reload permanent configuration into runtime
      firewall_cmd:
        state: reload

    - name: save runtime configuration to permanent configuration
      firewall_cmd:
        state: save

    - name: set zone as default
      firewall_cmd:
        default_zone: work
    - name: reset default zone
      firewall_cmd:
        default_zone: public

    - name: set log_denied to default
      firewall_cmd:
        log_denied: off

    - name: set automatic_helpers to default
      firewall_cmd:
        automatic_helpers: system
'''

RETURN = '''
firewalld:
    description: data structure showing the current configuration of firewalld
    returned: success
    type: complex
    contains:
        default_zone:
            description: default zone interfaces are placed in if they don't define ZONE in their ifcfg-* file
            returned: success
            type: string
            sample: public

        installed:
            description: true if the firewalld service is installed
            returned: success
            type: bool
            sample: true

        log_denied:
            description: current setting of log_denied; see corresponding option
            returned: success
            type: str
            sample: off

        automatic_helpers:
            description: current setting of automatic_helpers; see corresponding option
            returned: success
            type: str
            sample: off

        permanent_direct_chains:
            description: direct chains defined in the permanent configuration
            returned: success
            type: complex
            contains:
                family:
                    description: family of the chain (ipv4, ipv6, eb)
                    returned: success
                    type: str
                    sample: ipv4
                table:
                    description: table of the chain
                    returned: success
                    type: str
                    sample: filter
                chain:
                    description: chain name
                    returned: success
                    type: str
                    sample: IN_public_allow
        permanent_direct_passthroughs:
            description: direct passthroughs defined in the permanent configuration
            returned: success
            type: complex
            contains:
                family:
                family:
                    description: family of the passthrough (ipv4, ipv6, eb)
                    returned: success
                    type: str
                    sample: ipv4
                passthrough:
                    description: passthrough definition
                    returned: success
                    type: str
                    sample: -A IN_test_allow -p tcp -m tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT
        permanent_direct_rules:
            description: direct rules defined in the permanent configuration
            returned: success
            type: complex
            contains:
                family:
                    description: family of the chain (ipv4, ipv6, eb)
                    returned: success
                    type: str
                    sample: ipv4
                table:
                    description: table of the chain
                    returned: success
                    type: str
                    sample: filter
                chain:
                    description: chain name
                    returned: success
                    type: str
                    sample: IN_public_allow
                priority:
                    description: priority of the rule
                    returned: success
                    type: int
                    sample: 0
                rule:
                    description: rule content
                    returned: success
                    type: str
                    sample: -m tcp -p tcp -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
        permanent_zones:
            description: zones defined in the permanent configuration
            returned: success
            type: complex
            contains:
                forward_ports:
                    description: current setting of forward_ports; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['port=3389:proto=tcp:toport=3389:toaddr=192.168.42.42']
                icmp_block_inversion:
                    description: current setting of icmp_block_inversion; see corresponding option
                    returned: success
                    type: bool
                    sample: false
                icmp_blocks:
                    description: current setting of icmp_blocks; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['echo-request']
                interfaces:
                    description: current setting of interfaces; see corresponding option
                    returned: success
                    type: list(str)
                    sample:
                masquerade:
                    description: true if this zone is masquerading
                    returned: success
                    type: bool
                    sample: true
                name:
                    description: name of the zone
                    returned: success
                    type: str
                    sample: public
                permanent:
                    description: true if this is in the permanent configuration
                    returned: success
                    type: list(str)
                    sample: true
                ports:
                    description: current setting of ports; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['22/tcp']
                protocols:
                    description: current setting of protocols; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['gre']
                rich_rules:
                    description: current setting of rich_rules; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['rule protocol value="ah" accept']
                services:
                    description: current setting of services; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['ssh']
                source_ports:
                    description: current setting of source_ports; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['68/udp']
                sources:
                    description: current setting of sources; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['192.168.0.0/16']
                target:
                    description: current setting of target; see corresponding option
                    returned: success
                    type: str
                    sample: REJECT

        running:
            description: true if the firewalld service is running
            returned: success
            type: bool
            sample: true

        runtime_direct_chains:
            description: direct chains defined in the runtime configuration
            returned: success
            type: complex
            content:
                family:
                    description: family of the chain (ipv4, ipv6, eb)
                    returned: success
                    type: str
                    sample: ipv4
                table:
                    description: table of the chain
                    returned: success
                    type: str
                    sample: filter
                chain:
                    description: chain name
                    returned: success
                    type: str
                    sample: IN_public_allow
        runtime_direct_passthroughs:
            description: direct passthroughs defined in the runtime configuration
            returned: success
            type: complex
            contains:
                family:
                family:
                    description: family of the passthrough (ipv4, ipv6, eb)
                    returned: success
                    type: str
                    sample: ipv4
                passthrough:
                    description: passthrough definition
                    returned: success
                    type: str
                    sample: -A IN_test_allow -p tcp -m tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT
        runtime_direct_rules:
            description: direct rules defined in the runtime configuration
            returned: success
            type: complex
            contains:
                family:
                    description: family of the chain (ipv4, ipv6, eb)
                    returned: success
                    type: str
                    sample: ipv4
                table:
                    description: table of the chain
                    returned: success
                    type: str
                    sample: filter
                chain:
                    description: chain name
                    returned: success
                    type: str
                    sample: IN_public_allow
                priority:
                    description: priority of the rule
                    returned: success
                    type: int
                    sample: 0
                rule:
                    description: rule content
                    returned: success
                    type: str
                    sample: -m tcp -p tcp -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
        runtime_zones:
            description: zones defined in the runtime configuration
            returned: success
            type: complex
            contains:
                forward_ports:
                    description: current setting of forward_ports; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['port=3389:proto=tcp:toport=3389:toaddr=192.168.42.42']
                icmp_block_inversion:
                    description: current setting of icmp_block_inversion; see corresponding option
                    returned: success
                    type: bool
                    sample: false
                icmp_blocks:
                    description: current setting of icmp_blocks; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['echo-request']
                interfaces:
                    description: current setting of interfaces; see corresponding option
                    returned: success
                    type: list(str)
                    sample:
                masquerade:
                    description: true if this zone is masquerading
                    returned: success
                    type: bool
                    sample: true
                name:
                    description: name of the zone
                    returned: success
                    type: str
                    sample: public
                permanent:
                    description: true if this is in the permanent configuration
                    returned: success
                    type: list(str)
                    sample: true
                ports:
                    description: current setting of ports; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['22/tcp']
                protocols:
                    description: current setting of protocols; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['gre']
                rich_rules:
                    description: current setting of rich_rules; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['rule protocol value="ah" accept']
                services:
                    description: current setting of services; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['ssh']
                source_ports:
                    description: current setting of source_ports; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['68/udp']
                sources:
                    description: current setting of sources; see corresponding option
                    returned: success
                    type: list(str)
                    sample: ['192.168.0.0/16']
                target:
                    description: current setting of target; see corresponding option
                    returned: success
                    type: str
                    sample: REJECT

        version:
            description: version of firewalld
            returned: success
            type: str
            sample: '0.4.3.2'

            "permanent_zones": {
                "block": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "block",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [],
                    "source_ports": [],
                    "sources": [],
                    "target": "REJECT"
                },
                "dmz": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "dmz",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "drop": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "drop",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [],
                    "source_ports": [],
                    "sources": [],
                    "target": "DROP"
                },
                "external": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": true,
                    "name": "external",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "home": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "home",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "dhcpv6-client",
                        "mdns",
                        "samba-client",
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "internal": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "internal",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "dhcpv6-client",
                        "mdns",
                        "samba-client",
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "public": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "public",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "dhcpv6-client",
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "trusted": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "trusted",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [],
                    "source_ports": [],
                    "sources": [],
                    "target": "ACCEPT"
                },
                "work": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "work",
                    "permanent": true,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "dhcpv6-client",
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                }
            },
            "running": true,
            "runtime_direct_chains": [],
            "runtime_direct_passthroughs": [],
            "runtime_direct_rules": [],
            "runtime_zones": {
                "block": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "block",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [],
                    "source_ports": [],
                    "sources": [],
                    "target": "REJECT"
                },
                "dmz": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "dmz",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "drop": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "drop",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [],
                    "source_ports": [],
                    "sources": [],
                    "target": "DROP"
                },
                "external": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": true,
                    "name": "external",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "home": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "home",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "ssh",
                        "mdns",
                        "samba-client",
                        "dhcpv6-client"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "internal": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "internal",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "ssh",
                        "mdns",
                        "samba-client",
                        "dhcpv6-client"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "public": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [
                        "eth0"
                    ],
                    "masquerade": false,
                    "name": "public",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "dhcpv6-client",
                        "ssh"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                },
                "trusted": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "trusted",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [],
                    "source_ports": [],
                    "sources": [],
                    "target": "ACCEPT"
                },
                "work": {
                    "forward_ports": [],
                    "icmp_block_inversion": false,
                    "icmp_blocks": [],
                    "interfaces": [],
                    "masquerade": false,
                    "name": "work",
                    "permanent": false,
                    "ports": [],
                    "protocols": [],
                    "rich_rules": [],
                    "services": [
                        "ssh",
                        "dhcpv6-client"
                    ],
                    "source_ports": [],
                    "sources": [],
                    "target": "default"
                }
            },
            "version": "0.4.3.2"
        }
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.firewall_cmd_utils import FirewallCmdAnsibleModule
import re


def set_option(module, query_arg, set_arg, option):
    changed = False
    value = module.firewall_cmd([query_arg]).strip()

    if option != value:
        # if state will change, set changed true
        changed = True
        if not module.check_mode:
            module.firewall_cmd(["{0}={1}".format(set_arg, option)]).strip()

    return changed

def main():
    # set up the module & defaults
    module = FirewallCmdAnsibleModule(
        argument_spec=dict(
            default_zone=dict(type='str'),
            log_denied=dict(type='str', choices=['all', 'unicast', 'broadcast', 'multicast', 'off']),
            automatic_helpers=dict(type='str', choices=['yes', 'no', 'system']),
            state=dict(type='str', choices=['save', 'reload', 'complete-reload', 'get', 'get_version']),
        ),
        supports_check_mode=True
    )

    # check for get
    if module.params['state'] is not None and module.params['state'] == 'get':
        result = {'changed': False, 'firewalld':{}}

        if not module.firewalld_installed():
            result['firewalld']['installed'] = False
            module.exit_json(**result)
        else:
            result['firewalld']['installed'] = True

        if not module.firewalld_running():
            result['firewalld']['running'] = False
            module.exit_json(**result)
        else:
            result['firewalld']['running'] = True

        result['firewalld']['version'] = module.firewalld_version()
        result['firewalld']['log_denied'] = module.firewall_cmd(['--get-log-denied']).strip()
        if module.version_cmp('0.4.3.2', module.firewalld_version()) > 0:
            result['firewalld']['automatic_helpers'] = module.firewall_cmd(['--get-automatic-helpers']).strip()
        result['firewalld']['default_zone'] = module.firewall_cmd(['--get-default-zone']).strip()

        result['firewalld']['permanent_zones'] = {}
        result['firewalld']['runtime_zones'] = {}
        for permanent in (True, False):
            if permanent:
                zone_names = module.firewall_cmd(['--permanent', '--get-zones']).strip().split()
            else:
                zone_names = module.firewall_cmd(['--get-zones']).strip().split()

            for zone_name in zone_names:
                zone = {}
                zone['name'] = zone_name
                zone['permanent'] = permanent

                if permanent:
                    args = ['--permanent', '--zone=' + zone_name]
                else:
                    args = ['--zone=' + zone_name]

                perm_args = args[:]
                perm_args.append('--permanent')
                if module.version_cmp('0.4.3.2', module.firewalld_version()) > 0:
                    zone['description'] = module.firewall_cmd(perm_args + ['--get-description']).strip()
                    zone['short'] = module.firewall_cmd(perm_args + ['--get-short']).strip()
                zone['target'] = module.firewall_cmd(perm_args + ['--get-target']).strip()
                zone['icmp_block_inversion'] = module.firewall_cmd(args + ['--query-icmp-block-inversion']).strip() == 'yes'
                zone['interfaces'] = module.firewall_cmd(args + ['--list-interfaces']).strip().split()
                zone['sources'] = module.firewall_cmd(args + ['--list-sources']).strip().split()
                zone['services'] = module.firewall_cmd(args + ['--list-services']).strip().split()
                zone['ports'] = module.firewall_cmd(args + ['--list-ports']).strip().split()
                zone['protocols'] = module.firewall_cmd(args + ['--list-protocols']).strip().split()
                zone['masquerade'] = module.firewall_cmd(args + ['--query-masquerade']).strip() == 'yes'

                zone['forward_ports'] = []
                for line in module.firewall_cmd(args + ['--list-forward-ports']).strip().splitlines():
                    line = line.strip()
                    if line != '':
                        zone['forward_ports'].append(line)

                zone['source_ports'] = module.firewall_cmd(args + ['--list-source-ports']).strip().split()
                zone['icmp_blocks'] = module.firewall_cmd(args + ['--list-icmp-blocks']).strip().split()

                zone['rich_rules'] = []
                for line in module.firewall_cmd(args + ['--list-rich-rules']).splitlines():
                    line = line.strip()
                    if line != '':
                        zone['rich_rules'].append(line)

                if permanent:
                    result['firewalld']['permanent_zones'][zone_name] = zone
                else:
                    result['firewalld']['runtime_zones'][zone_name] = zone

            if permanent:
                args = ['--permanent', '--direct']
            else:
                args = ['--direct']

            direct_rules = []
            for line in module.firewall_cmd(args + ['--get-all-rules']).splitlines():
                m = re.match(r'^(ipv4|ipv6|eb) (\S+) (\S+) ([0-9]+) (.*)$', line.strip())
                if m:
                    direct_rules.append(
                        dict(
                            family=m.group(1),
                            table=m.group(2),
                            chain=m.group(3),
                            priority=m.group(4),
                            rule=m.group(5)
                        )
                    )

            direct_passthroughs = []
            for line in module.firewall_cmd(args + ['--get-all-passthroughs']).splitlines():
                m = re.match(r'^(ipv4|ipv6|eb) (.*)$', line.strip())
                if m:
                    direct_passthroughs.append(
                        dict(
                            family=m.group(1),
                            passthrough=m.group(2)
                        )
                    )
            direct_chains = []
            for line in module.firewall_cmd(args + ['--get-all-chains']).splitlines():
                m = re.match(r'^(ipv4|ipv6|eb) (\S+) (\S+)$', line.strip())
                if m:
                    direct_passthroughs.append(
                        dict(
                            family=m.group(1),
                            table=m.group(2),
                            chain=m.group(3)
                        )
                    )
            if permanent:
                result['firewalld']['permanent_direct_chains'] = direct_chains
                result['firewalld']['permanent_direct_rules'] = direct_rules
                result['firewalld']['permanent_direct_passthroughs'] = direct_passthroughs
            else:
                result['firewalld']['runtime_direct_chains'] = direct_chains
                result['firewalld']['runtime_direct_rules'] = direct_rules
                result['firewalld']['runtime_direct_passthroughs'] = direct_passthroughs

        module.exit_json(**result)

    # check for get_version
    if module.params['state'] is not None and module.params['state'] == 'get_version':
        result = {'changed': False, 'firewalld':{}}

        if not module.firewalld_installed():
            result['firewalld']['installed'] = False
            module.exit_json(**result)
        else:
            result['firewalld']['installed'] = True

        if not module.firewalld_running():
            result['firewalld']['running'] = False
            module.exit_json(**result)
        else:
            result['firewalld']['running'] = True

        result['firewalld']['version'] = module.firewalld_version()

        module.exit_json(**result)

    if not module.firewalld_installed():
        module.fail_json(msg='firewalld is not installed')
    if not module.firewalld_running():
        module.fail_json(msg='firewalld is not running')

    # check for save
    if module.params['state'] is not None and module.params['state'] == 'save':
        module.firewall_cmd(['--runtime-to-permanent'])

        # TODO figure out if runtime & perm are different
        module.exit_json(changed=True)

    # check for reload
    if module.params['state'] is not None and module.params['state'] == 'reload':
        module.firewall_cmd(['--reload'])

        # TODO figure out if runtime & perm are different
        module.exit_json(changed=True)


    # check for complete-reload
    if module.params['state'] is not None and module.params['state'] == 'complete-reload':
        module.firewall_cmd(['--complete-reload'])

        # TODO figure out if runtime & perm are different
        module.exit_json(changed=True)

    result = {'changed': False}

    if module.params['log_denied'] is not None and set_option(
        module,
        '--get-log-denied',
        '--set-log-denied',
        module.params['log_denied']
    ):
        result['changed'] = True

    if (
        module.version_cmp('0.4.3.2', module.firewalld_version()) <= 0
        and module.params['automatic_helpers'] is not None
    ):
        module.fail_json(msg='The "automatic helpers" feature is not available in firewalld ' + module.firewalld_version())
    elif module.params['automatic_helpers'] is not None and set_option(
        module,
        '--get-automatic-helpers',
        '--set-automatic-helpers',
        module.params['automatic_helpers']
    ):
        result['changed'] = True


    if module.params['default_zone'] is not None and set_option(
        module,
        '--get-default-zone',
        '--set-default-zone',
        module.params['default_zone']
    ):
        result['changed'] = True

    module.exit_json(**result)

if __name__ == '__main__':
    main()
