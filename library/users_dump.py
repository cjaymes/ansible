#!/usr/bin/python

# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: passwd_dump
short_description: Parse the passwd file
description:
  - Get the parsed contents of the passwd file.
version_added: "2.5"
author: "Casey Jaymes"
options:
'''

EXAMPLES = '''
    - name: parse passwd file
      passwd_dump:
      register: passwd
    - debug:
        msg: '{{passwd}}'
'''

RETURN = '''
users:
    description: data structure corresponding to the users on the system
    returned: success
    type: list(dict)
    contains:
        name:
            description: Login of the user.
            returned: success
            type: str
            sample: root
        uid:
            description: The ID of the user.
            returned: success
            type: int
            sample: 0
        gid:
            description: The primary group ID of the user.
            returned: success
            type: int
            sample: 0
        comment:
            description: Comment field. Usually the user's full name.
            returned: success
            type: string
            sample: Root User
        home:
            description: The home directory of the user.
            returned: success
            type: str
            sample: /root
        shell:
            description: The shell spawned for the user. /sbin/nologin can be used for users not able to log in.
            returned: success
            type: str
            sample: /bin/bash
users_by_id:
    description: Same as users, but indexed by id. See users for format of the inner dict.
    returned: success
    type: dict(int, dict)
users_by_name:
    description: Same as users, but indexed by name. See users for format of the inner dict.
    returned: success
    type: dict(str, dict)
groups:
    description: data structure corresponding to the groups on the system
    returned: success
    type: list(dict)
    contains:
        group:
            description: Name of the group.
            returned: success
            type: str
            sample: users
        gid:
            description: The group ID.
            returned: success
            type: int
            sample: 0
        members:
            description: The members of the group
            returned: success
            type: list(str)
            sample: ['user1', 'user2']
groups_by_id:
    description: Same as groups, but indexed by id. See groups for format of the inner dict.
    returned: success
    type: dict(int, dict)
groups_by_name:
    description: Same as groups, but indexed by name. See groups for format of the inner dict.
    returned: success
    type: dict(str, dict)
login_defs:
    description: Settings from /etc/login.defs
    returned: success
    type: dict(str, str)
'''

from ansible.module_utils.basic import AnsibleModule
import re


def main():
    # set up the module & defaults
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    result = {'changed': False}

    result['login_defs'] = {}
    try:
        rc, out, err = module.run_command(['cat', '/etc/login.defs'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/login.defs failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/login.defs failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = re.sub(r'^(.*)#.*$', '\\1', line)
        line = line.strip()
        if line == '':
            continue

        print(line)
        key, value = line.split(None, 1)
        result['login_defs'][key] = value

    if 'UID_MIN' not in result['login_defs']:
        module.fail_json(msg='/etc/login.defs did not contain UID_MIN')
    if 'UID_MAX' not in result['login_defs']:
        module.fail_json(msg='/etc/login.defs did not contain UID_MAX')

    UID_MIN = int(result['login_defs']['UID_MIN'])
    UID_MAX = int(result['login_defs']['UID_MAX'])
    GID_MIN = int(result['login_defs']['GID_MIN'])
    GID_MAX = int(result['login_defs']['GID_MAX'])

    result['groups'] = []
    result['groups_by_name'] = {}
    result['groups_by_id'] = {}
    try:
        rc, out, err = module.run_command(['cat', '/etc/group'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/group failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/group failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = re.sub(r'^(.*)#.*$', '\\1', line)
        line = line.strip()

        if line == '':
            continue

        name, pw, gid, members = line.split(':', 3)
        gid = int(gid)
        members = members.split(',')
        record = dict(name=name, gid=gid, members=members, is_sys=is_sys)
        result['groups'].append(record)
        result['groups_by_name'][name] = record
        result['groups_by_id'][gid] = record

    result['users'] = []
    result['users_by_name'] = {}
    result['users_by_id'] = {}
    try:
        rc, out, err = module.run_command(['cat', '/etc/passwd'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/passwd failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/passwd failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = re.sub(r'^(.*)#.*$', '\\1', line)

        line = line.strip()

        if line == '':
            continue

        name, pw, uid, gid, comment, home, shell = line.split(':')
        uid = int(uid)
        if uid >= UID_MIN and uid < UID_MAX:
            is_interactive = True
            is_sys = False
        else:
            is_interactive = False
            is_sys = True

        gid = int(gid)

        if gid not in result['groups_by_id']:
            module.fail_json(msg='Unable to match user primary group {0} with /etc/group file'.format(str(gid)))
        result['groups_by_id']['members'].append(name)

        record = dict(name=name, uid=uid, gid=gid, comment=comment, home=home,
            shell=shell, is_sys=is_sys)
        result['users'].append(record)
        result['users_by_name'][name] = record
        result['users_by_id'][uid] = record

    try:
        rc, out, err = module.run_command(['cat', '/etc/shadow'])
        if len(err) > 0:
            module.fail_json(msg='cat /etc/shadow failed with error: {0}'.format(str(err)))
    except OSError as exception:
        module.fail_json(msg='cat /etc/shadow failed with exception: {0}'.format(exception))

    for line in out.splitlines():
        line = re.sub(r'^(.*)#.*$', '\\1', line)

        line = line.strip()

        if line == '':
            continue

        login, passwd, lastchg, mindays, maxdays, warndays, inactive, expire, reserved = line.split(':')

        if login not in result['users_by_name']:
            module.fail_json(msg='Unable to find user {0} from /etc/shadow'.format(login))

        result['users_by_name'][login]['no_passwd'] = passwd == ''
        result['users_by_name'][login]['disabled'] = passwd == '*'
        result['users_by_name'][login]['locked'] = passwd.startswith('!')

        result['users_by_name'][login]['lastchg'] = int(lastchg)
        result['users_by_name'][login]['mindays'] = int(mindays)
        result['users_by_name'][login]['maxdays'] = int(maxdays)
        result['users_by_name'][login]['warndays'] = int(warndays)
        result['users_by_name'][login]['inactive'] = int(inactive)
        result['users_by_name'][login]['expire'] = int(expire)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
