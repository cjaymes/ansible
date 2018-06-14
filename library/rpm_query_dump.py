#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: rpm_query_dump
short_description: Parse the output of rpm --query --dump for a package
description:
  - Get the parsed contents of the rpm --query --dump <package>.
version_added: "2.5"
author: "Casey Jaymes"
options:
    name:
        description:
            - The name of the package to query.
        type: str
'''

EXAMPLES = '''
    - name: parse rpm --query --dump
      rpm_query_dump:
        name: kernel
      register: rpm_query_dump
    - debug:
        msg: '{{rpm_query_dump}}'
'''

RETURN = '''
rpm_query_dump:
    description: data structure corresponding to the fields in rpm --query --dump
    returned: success
    type: list(dict)
    contains:
        path:
            description: Path of the file.
            returned: success
            type: str
            sample: /lib/modules/3.10.0-862.el7.x86_64/kernel/sound/x86/snd-hdmi-lpe-audio.ko.xz
        size:
            description: File size, in bytes.
            returned: success
            type: int
            sample: 11736
        mtime:
            description: File mtime: last modified time, in seconds past the Unix zero date of January 1, 1970.
            returned: success
            type: int
            sample: 1521673177
        digest:
            description: File digest: the checksum of the file's contents.
            returned: success
            type: str
            sample: f22ef4b3b3417378bab23a38f021d5309f53d8b930649386d468634348a755fe
        mode:
            description: File mode.
            returned: success
            type: int
            sample: 0100644
        mode_type:
            description: File type. One of directory, character, block, regular, fifo, link, or socket.
            returned: success
            type: str
            sample: directory
        mode_is_directory:
            description: True when file is a directory.
            returned: success
            type: bool
            sample: True
        mode_is_character:
            description: True when file is a character special device.
            returned: success
            type: bool
            sample: True
        mode_is_block:
            description: True when file is a block special device.
            returned: success
            type: bool
            sample: True
        mode_is_regular:
            description: True when file is a regular file.
            returned: success
            type: bool
            sample: True
        mode_is_fifo:
            description: True when file is a FIFO pipe.
            returned: success
            type: bool
            sample: True
        mode_is_link:
            description: True when file is a symbolic link.
            returned: success
            type: bool
            sample: True
        mode_is_socket:
            description: True when file is a socket.
            returned: success
            type: bool
            sample: True
        mode_permissions:
            description: Permission part of the file mode, including setuid, setguid and sticky bits.
            returned: success
            type: int
            sample: 0o0755
        mode_is_socket:
            description: True when file is a socket.
            returned: success
            type: bool
            sample: True
        mode_is_setuid:
            description: True when setuid is set.
            returned: success
            type: bool
            sample: True
        mode_is_setgid:
            description: True when setgid is set.
            returned: success
            type: bool
            sample: True
        mode_is_sticky:
            description: True when the stick bit is set.
            returned: success
            type: bool
            sample: True
        mode_owner:
            description: 3 bits defining the owner's permissions.
            returned: success
            type: int
            sample: 7
        mode_group:
            description: 3 bits defining the group owner's permissions.
            returned: success
            type: int
            sample: 5
        mode_other:
            description: 3 bits defining the other permissions.
            returned: success
            type: int
            sample: 5
        mode_owner_read:
            description: True when owner can read file.
            returned: success
            type: bool
            sample: True
        mode_owner_write:
            description: True when owner can write file.
            returned: success
            type: bool
            sample: True
        mode_owner_execute:
            description: True when owner can execute file.
            returned: success
            type: bool
            sample: True
        mode_group_read:
            description: True when group owners can read file.
            returned: success
            type: bool
            sample: True
        mode_group_write:
            description: True when group owners can write file.
            returned: success
            type: bool
            sample: True
        mode_group_execute:
            description: True when group owners can execute file.
            returned: success
            type: bool
            sample: True
        mode_other_read:
            description: True when anyone can read file.
            returned: success
            type: bool
            sample: True
        mode_other_write:
            description: True when anyone can write to file.
            returned: success
            type: bool
            sample: True
        mode_other_execute:
            description: True when anyone can execute file.
            returned: success
            type: bool
            sample: True
        user:
            description: File user owner.
            returned: success
            type: str
            sample: root
        group:
            description: File group owner.
            returned: success
            type: str
            sample: root
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
        device_major_minor:
            description: Device major, minor numbers.
            returned: success
            type: int
            sample: 0
        device_major:
            description: Device major numbers.
            returned: success
            type: int
            sample: 0
        device_minor:
            description: Device minor numbers.
            returned: success
            type: int
            sample: 0
        link_path:
            description: Link path.
            returned: success
            type: str
            sample: base
'''

from ansible.module_utils.basic import AnsibleModule
import os
import re
import stat


def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True)
        ),
        supports_check_mode=True
    )

    result = {'changed': False, 'rpm_query_dump': []}

    try:
        rc, out, err = module.run_command(['rpm', '--query', '--dump', module.params['name']])
        if len(err) > 0:
            module.fail_json(msg='rpm --query --dump failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='rpm --query --dump failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = line.strip()

        if line == '':
            continue

        (path, size, mtime, checksum, mode, user, group, is_config, is_doc, device_major_minor, link_path) = line.split()
        size = int(size)
        mtime = int(mtime)
        mode = int(mode, 8)
        device_major_minor = int(device_major_minor)

        record = {}

        record['path'] = path

        record['size'] = size

        record['mtime'] = mtime

        record['checksum'] = checksum

        record['mode'] = mode
        record['mode_is_directory'] = stat.S_ISDIR(mode)
        if record['mode_is_directory']:
            record['mode_type'] = 'directory'
        record['mode_is_character'] = stat.S_ISCHR(mode)
        if record['mode_is_character']:
            record['mode_type'] = 'character'
        record['mode_is_block'] = stat.S_ISBLK(mode)
        if record['mode_is_block']:
            record['mode_type'] = 'block'
        record['mode_is_regular'] = stat.S_ISREG(mode)
        if record['mode_is_regular']:
            record['mode_type'] = 'regular'
        record['mode_is_fifo'] = stat.S_ISFIFO(mode)
        if record['mode_is_fifo']:
            record['mode_type'] = 'fifo'
        record['mode_is_link'] = stat.S_ISLNK(mode)
        if record['mode_is_link']:
            record['mode_type'] = 'link'
        record['mode_is_socket'] = stat.S_ISSOCK(mode)
        if record['mode_is_socket']:
            record['mode_type'] = 'socket'
        record['mode_permissions'] = stat.S_IMODE(mode)
        record['mode_is_setuid'] = mode & stat.S_ISUID
        record['mode_is_setgid'] = mode & stat.S_ISGID
        record['mode_is_sticky'] = mode & stat.S_ISVTX
        record['mode_owner'] = mode & stat.S_IRWXU
        record['mode_group'] = mode & stat.S_IRWXG
        record['mode_other'] = mode & stat.S_IRWXO
        record['mode_owner_read'] = mode & stat.S_IRUSR
        record['mode_owner_write'] = mode & stat.S_IWUSR
        record['mode_owner_execute'] = mode & stat.S_IXUSR
        record['mode_group_read'] = mode & stat.S_IRGRP
        record['mode_group_write'] = mode & stat.S_IWGRP
        record['mode_group_execute'] = mode & stat.S_IXGRP
        record['mode_other_read'] = mode & stat.S_IROTH
        record['mode_other_write'] = mode & stat.S_IWOTH
        record['mode_other_execute'] = mode & stat.S_IXOTH

        record['user'] = user

        record['group'] = group

        record['is_config'] = is_config == '1'

        record['is_doc'] = is_doc == '1'

        record['device_major_minor'] = device_major_minor
        record['device_major'] = os.major(device_major_minor)
        record['device_minor'] = os.minor(device_major_minor)

        if link_path.upper() == 'X':
            record['link_path'] = None
        else:
            record['link_path'] = link_path

        result['rpm_query_dump'].append(record)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
