#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: exports_dump
short_description: Parse the exports file
description:
  - Get the parsed contents of the exports file.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
    - name: parse exports file
      exports_dump:
      register: exports
    - debug:
        msg: '{{exports}}'
'''

RETURN = '''
exports:
    description: data structure corresponding to the fields in the exports file
    returned: success
    type: dict(dict)
    contains:
'''

from ansible.module_utils.basic import AnsibleModule
import re


def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    result = {'changed': False, 'exports': {}}

    try:
        rc, out, err = module.run_command(['cat', '/etc/exports'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/exports failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/exports failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = line.strip()

        # remove comments
        line = re.sub(r'#.*$', '', line)

        if line == '':
            continue

        (export, clientlist) = re.split(r'\s+', line, maxsplit=1)
        result['exports'][export] = []

        default_opts = []
        for clientspec in re.split(r'\s+', clientlist):
            if clientspec.startswith('-'):
                default_opts = clientspec[1:].split(',')
            elif '(' in clientspec:
                (client, opts) = clientspec[:-1].split('(')
                options = default_opts[:]
                options.extend(opts.split(','))
                result['exports'][export].append(dict(client=client, options=options))
            else:
                options = default_opts[:]
                result['exports'][export].append(dict(client=clientspec, options=options))

    module.exit_json(**result)

if __name__ == '__main__':
    main()
