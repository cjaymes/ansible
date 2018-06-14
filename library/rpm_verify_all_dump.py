#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: rpm_verify_all_dump
short_description: Parse the output of rpm --verify --all
description:
  - Get the parsed contents of the rpm --verify --all.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
    - name: parse rpm --verify --all
      rpm_verify_all_dump:
      register: rpm_verify_all
    - debug:
        msg: '{{rpm_verify_all}}'
'''

RETURN = '''
rpm_verify_all:
    description: data structure corresponding to the fields in rpm --verify --all
    returned: success
    type: list(dict)
    contains:
        size_differs:
            description: True when file size differs.
            returned: success
            type: bool
            sample: True
        mode_differs:
            description: True when file mode differs, including permissions and file type.
            returned: success
            type: bool
            sample: True
        digest_differs:
            description: True when file digest differs.
            returned: success
            type: bool
            sample: True
        device_major_minor_mismatch:
            description: True when device major/minor number mismatch.
            returned: success
            type: bool
            sample: True
        link_path_mismatch:
            description: True when link path mismatch.
            returned: success
            type: bool
            sample: True
        owner_differs:
            description: True when file user ownership differs.
            returned: success
            type: bool
            sample: True
        group_differs:
            description: True when file group ownership differs.
            returned: success
            type: bool
            sample: True
        mtime_differs:
            description: True when file mtime differs.
            returned: success
            type: bool
            sample: True
        caps_differ:
            description: True when capabilities differ.
            returned: success
            type: bool
            sample: True
        is_config:
            description: True when path is a configuration file.
            returned: success
            type: bool
            sample: False
        is_doc:
            description: True when path is a documentation file.
            returned: success
            type: bool
            sample: False
        is_ghost:
            description: True when path contents were not included in package.
            returned: success
            type: bool
            sample: False
        is_license:
            description: True when path is a license file.
            returned: success
            type: bool
            sample: False
        is_readme:
            description: True when path is a README file.
            returned: success
            type: bool
            sample: False
        path:
            description: Path of the file.
            returned: success
            type: str
            sample: /etc/audit/audit.rules.d/audit.rules
'''

from ansible.module_utils.basic import AnsibleModule
import re


def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    result = {'changed': False, 'rpm_verify_all': []}

    try:
        rc, out, err = module.run_command(['rpm', '--verify', '--all'])
        if len(err) > 0:
            module.fail_json(msg='rpm --verify --all failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='rpm --verify --all failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = line.strip()

        if line == '':
            continue

        m = re.match(r'^([S.])([M.])([5.])([D.])([L.])([U.])([G.])([T.])([P.])\s+([ cdglr])\s+(.*)$', line)
        if not m:
            continue

        record = {}
        record['size_differs'] = m.group(1) == 'S'
        record['mode_differs'] = m.group(2) == 'M'
        record['digest_differs'] = m.group(3) == '5'
        record['device_major_minor_mismatch'] = m.group(4) == 'D'
        record['link_path_mismatch'] = m.group(5) == 'L'
        record['owner_differs'] = m.group(6) == 'U'
        record['group_differs'] = m.group(7) == 'G'
        record['mtime_differs'] = m.group(8) == 'T'
        record['caps_differ'] = m.group(9) == 'P'

        record['is_config'] = m.group(10) == 'c'
        record['is_doc'] = m.group(10) == 'd'
        record['is_ghost'] = m.group(10) == 'g'
        record['is_license'] = m.group(10) == 'l'
        record['is_readme'] = m.group(10) == 'r'

        record['path'] = m.group(11)

        result['rpm_verify_all'].append(record)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
