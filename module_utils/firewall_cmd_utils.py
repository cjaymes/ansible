# (c) 2018, Casey Jaymes (Github @cjaymes)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
import re


class FirewallCmdAnsibleModule(AnsibleModule):
    __VERSION = None

    def firewalld_installed(self):
        try:
            rc, out, err = self.run_command("which firewall-cmd", use_unsafe_shell=True)
            if len(err) > 0:
                return False
        except OSError as exception:
            return False
        return True

    def firewalld_running(self):
        try:
            rc, out, err = self.run_command("firewall-cmd --state", use_unsafe_shell=True)
            if len(err) > 0:
                return False
        except OSError as exception:
            return False
        if out.strip() != 'running':
            return False
        return True

    def firewalld_version(self):
        if self.__VERSION is None:
            self.__VERSION = self.firewall_cmd(['-V']).strip()
        return self.__VERSION

    # from https://stackoverflow.com/questions/1714027/version-number-comparison-in-python
    def version_cmp(self, version1, version2):
        def normalize(v):
            return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
        return cmp(normalize(version1), normalize(version2))

    def firewall_cmd(self, cmd):
        cmd.insert(0, 'firewall-cmd')
        try:
            rc, out, err = self.run_command(cmd)
            if len(err) > 0:
                self.fail_json(msg='firewall-cmd failed with error: {0}'.format(str(err)))
        except OSError as exception:
            self.fail_json(msg='firewall-cmd failed with exception: {0}'.format(exception))
        return out

    def firewalld_get_result(self):
        result = {'changed': False, 'firewalld':{}}

        if not self.firewalld_installed():
            result['firewalld']['installed'] = False
            self.exit_json(**result)
        else:
            result['firewalld']['installed'] = True

        if not self.firewalld_running():
            result['firewalld']['running'] = False
            self.exit_json(**result)
        else:
            result['firewalld']['running'] = True

        result['firewalld']['version'] = self.firewalld_version()
        result['firewalld']['log_denied'] = self.firewall_cmd(['--get-log-denied']).strip()
        if self.version_cmp('0.4.3.2', self.firewalld_version()) > 0:
            result['firewalld']['automatic_helpers'] = self.firewall_cmd(['--get-automatic-helpers']).strip()
        result['firewalld']['default_zone'] = self.firewall_cmd(['--get-default-zone']).strip()
        result['firewalld']['permanent_zones'] = self.firewall_cmd(['--permanent', '--get-zones']).strip().split()
        result['firewalld']['runtime_zones'] = self.firewall_cmd(['--permanent', '--get-zones']).strip().split()

        return result
