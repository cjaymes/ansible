#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: fstab_dump
short_description: Parse the fstab file
description:
  - Get the parsed contents of the fstab file.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
    - name: parse fstab file
      fstab_dump:
      register: fstab
    - debug:
        msg: '{{fstab}}'
'''

RETURN = '''
fstab:
    description: data structure corresponding to the fields in the fstab file
    returned: success
    type: list(dict)
    contains:
        device:
            description: The device or partition that contains the file system
            returned: success
            type: string
            sample: /dev/sda1
        mount_point:
            description: The directory (aka mount point) on whice to make the files system accessible
            returned: success
            type: string
            sample: /boot
        fstype:
            description: The file system type
            returned: success
            type: string
            sample: xfs
        options:
            description: The options fed to the mount command when mounting the file system
            returned: success
            type: string
            sample: defaults
        dump:
            description: 0 to disable backing up the file system. 1 to enable it.
            returned: success
            type: int
            sample: 0
        pass:
            description: The order in which fsck checks file systems for errors at boot time. / should use 1, other file systems should be 2 or 0 disables checking
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

    result = {'changed': False, 'fstab': []}

    try:
        rc, out, err = module.run_command(['cat', '/etc/fstab'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/fstab failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/fstab failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        if re.match(r'^\s*#', line):
            continue

        line = line.strip()

        if line == '':
            continue

        record = zip(
            ('device', 'mount_point', 'fstype', 'options', 'dump', 'pass'),
            re.split(r'\s+', line, maxsplit=6)
        )
        record = dict(record)
        record['dump'] = int(record['dump'])
        record['pass'] = int(record['pass'])
        result['fstab'].append(record)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
