# Firewall
firewall-cmd --add-service=ssh
firewall-cmd --add-service=snmp
firewall-cmd --direct --add-rule ipv4 filter IN_drop_allow 0 -p tcp -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
firewall-cmd --runtime-to-permanent

# Sudoers
echo '%${dns_domain}\\LinuxAdmins ALL=(ALL) ALL' > /etc/sudoers.d/S01LinuxAdmins

# yum repository
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
mkdir /var/rhel7repo
echo '${repo_server}:/var/rhel7repo /var/rhel7repo nfs ro,nosuid 0 0' >> /etc/fstab
mount /var/rhel7repo
rm -f /etc/yum.repos.d/*
ln -s /var/rhel7repo/${repo_server} /etc/yum.repos.d/
yum erase -y subscription-manager rhn*
yum update -y

# ntp
systemctl stop chronyd chrony-wait
systemctl disable chronyd chrony-wait
yum erase -y chrony
userdel chrony

yum install -y ntp
sed -ri 's/^server/#server/g' /etc/ntp.conf
echo 'server ${ntp_server0} prefer
server ${ntp_server1} prefer
maxpoll 10' >> /etc/ntp.conf

# rng
cp /usr/lib/systemd/system/rngd.service /etc/systemd/system
sed -ri 's/^ExecStart(.*)$/ExecStart\1 -r \/dev\/urandom/' /etc/systemd/system/rngd.service

systemctl daemon-reload
systemctl restart rngd

# snmp
yum install -y net-snmp
## TODO configure user
#systemctl enable snmpd
#systemctl start snmpd

# usbguard
yum install -y usbguard

echo 'allow with-interface one-of { 03:00:01 03:01:01 }
allow with-interface one-of { 03:00:02 03:01:02 }
allow with-interface one-of { 09:00:00 09:00:01 09:00:02 }
allow with-interface equals { 0B:*:* }
reject
' > /etc/usbguard/rules.conf
chmod 0600 /etc/usbguard/rules.conf

sed -ri 's/^(ImplicitPolicyTarget)=.*$/\1=reject/' /etc/usbguard/usbguard-daemon.conf
sed -ri 's/^(Present.*Policy)=.*$/\1=apply-policy/' /etc/usbguard/usbguard-daemon.conf

systemctl start usbguard
systemctl enable usbguard

# stig
for f in `rpm -Va | grep '^.M' | awk '{print $3}'`; do
  pkg=`rpm -qf $f`
  rpm --setperms $pkg
  rpm --setugids $pkg
done

for line in `rpm -Va | grep '^.M'`; do
  config=`echo "$line" | awk '{print $2}'`
  f=`echo "$line" | awk '{print $3}'`
  pkg=`rpm -qf $f`
  yum reinstall $pkg
done

echo 'HostbasedAuthentication no' >> /etc/ssh/sshd_config

grub2-setpassword

grub2-mkconfig -o /etc/grub2.cfg

yum install -y policycoreutils-python

yum install -y aide
echo "0 0 * * * /usr/bin/aide --check | /bin/mail -s 'aide integrity check run for $(hostname)' root@$(hostname)" > /etc/cron.daily/aide
chmod 0755 /etc/cron.daily/aide

echo 'install usb-storage /bin/true' > /etc/modprobe.d/nousbstorage

userdel games
groupdel games
userdel ftp

systemctl disable kdump

sed -ri 's/^(FIPSR) = .*$/\1 = p+i+n+u+g+s+m+c+acl+selinux+xattrs+sha512/' /etc/aide.conf
sed -ri 's/^(NORMAL) = .*$/\1 = sha512/' /etc/aide.conf
sed -ri 's/^(CONTENT) = .*$/\1 = sha512+ftype/' /etc/aide.conf
sed -ri 's/^(CONTENT_EX) = .*$/\1 = sha512+ftype+p+u+g+n+acl+selinux+xattrs/' /etc/aide.conf
sed -ri 's/^(DATAONLY) = .*$/\1 = p+n+u+g+s+acl+selinux+xattrs+sha512/' /etc/aide.conf

systemctl enable tmp.mount

echo 'PRELINKING=no' > /etc/sysconfig/prelink
b=$(blkid $(mount | grep /boot | awk '{print $1}') | awk '{print $2}' | sed 's/"//g')
sed -ri "s/^(GRUB_CMDLINE_LINUX)=\"(.*)\"/\1=\"\2 fips=1 boot=$b\"/" /etc/default/grub
grub2-mkconfig -o /etc/grub2.cfg
yum install -y dracut-fips*
dracut -f

sed -ri 's/^(GRUB_CMDLINE_LINUX)="(.*)"/\1="\2 audit=1"/' /etc/default/grub
grub2-mkconfig -o /etc/grub2.cfg
cd /etc/audit/rules.d
rm -f audit.rules
echo '# Delete all rules
-D' > 00_delete.rules
echo '# Buffer size
-b 8192' > 01_buffer_size.rules
echo '# Shut down on failures
-f 2' > 02_failure_action.rules

yum install -y audispd-plugins
sed -ri 's/^(remote_server).*$/\1 = ${syslog_server}/' /etc/audisp/audisp-remote.conf

sed -ri 's/^(enable_krb5).*$/\1 = yes/' /etc/audisp/audisp-remote.conf

sed -ri 's/^(disk_full_action).*$/\1 = syslog/' /etc/audisp/audisp-remote.conf

sed -ri 's/^(network_failure_action).*$/\1 = syslog/' /etc/audisp/audisp-remote.conf

part_size=$(df /var/log/audit --block-size 1M -P | tail -n1 | awk '{print $2}')
s=$(echo "$part_size * 0.25 / 1" | bc)
sed -ri "s/^(space_left)\s*=.*$/\1 = $s/" /etc/audit/auditd.conf

sed -ri 's/^(space_left_action).*$/\1 = email/' /etc/audit/auditd.conf

cd /etc/audit/rules.d

for f in `find / -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null`; do
  echo "-a always,exit -F path=$f -F perm=x -F auid>=1000 -F auid!=4294967295 -k setuid/setgid" >> setuid_setgid.rules
done

for s in chown fchown lchown fchownat chmod fchmod fchmodat setxattr fsetxattr lsetxattr removexattr fremovexattr lremovexattr; do
  for a in b32 b64; do
    echo "-a always,exit -F arch=$a -S $s -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> perm_mod.rules
  done
done

for s in creat open openat open_by_handle_at truncate ftruncate; do
  for a in b32 b64; do
    echo "-a always,exit -F arch=$a -S $s -Fexit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access" >> access.rules
  done
done

for p in /usr/sbin/semanage /usr/sbin/setsebool /usr/bin/chcon /usr/sbin/restorecon; do
  echo "-a always,exit -F path=$p -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged-priv_change" >> privileged-priv_change.rules
done

for f in /var/log/tallylog /var/run/faillock /var/log/lastlog; do
  echo "-w $f -p wa -k logins" >> logins.rules
done

for p in /usr/bin/passwd /sbin/unix_chkpwd /usr/bin/gpasswd /usr/bin/chage /usr/sbin/userhelper /bin/su /usr/bin/sudo; do
  echo "-a always,exit -F path=$p -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged-passwd" >> privileged-passwd.rules
done

for f in /etc/sudoers /etc/sudoers.d; do
  echo "-w $f -p wa -k privileged-actions" >> privileged-actions.rules
done

for p in /usr/bin/newgrp /usr/bin/chsh /usr/bin/sudoedit; do
  echo "-a always,exit -F path=$p -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged-priv_change" >> privileged-priv_change.rules
done

for a in b32 b64; do
  echo "-a always,exit -F arch=$a -S mount -F auid>=1000 -F auid!=4294967295 -k privileged-mount" >> privileged-mount.rules
done
echo "-a always,exit -F path=/bin/umount -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged-mount" >> privileged-mount.rules

for p in /usr/sbin/postdrop /usr/sbin/postqueue; do
  echo "-a always,exit -F path=$p -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged-postfix" >> privileged-postfix.rules
done

echo "-a always,exit -F path=/usr/libexec/openssh/ssh-keysign -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged-ssh" >> privileged-ssh.rules

echo "-a always,exit -F path=/usr/libexec/pt_chown -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged_terminal" >> privileged_terminal.rules

echo "-a always,exit -F path=/usr/bin/crontab -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged-cron" >> privileged-cron.rules

echo "-a always,exit -F path=/sbin/pam_timestamp_check -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged-pam" >> privileged-pam.rules

for s in init_module delete_module; do
  for a in b32 b64; do
    echo "-a always,exit -F arch=$a -S $s -k module-change" >> module-change.rules
  done
done
for p in /sbin/insmod /sbin/rmmod /sbin/modprobe; do
  echo "-w $p -p x -F auid!=4294967295 -k module-change" >> module-change.rules
done

for f in /etc/passwd /etc/group /etc/gshadow /etc/shadow /etc/oppasswd; do
  echo "-w $f -p wa -k identity" >> identity.rules
done

for s in rename renameat rmdir unlink unlinkat; do
  for a in b32 b64; do
    echo "-a always,exit -F arch=$a -S $s -F perm=x -F auid>=1000 -F auid!=4294967295 -k delete" >> delete.rules
  done
done

#TODO configure log aggregation server
echo "*.* @@${syslog_server}" >> /etc/rsyslog.conf

sed -ri 's/^(Ciphers) .*$/\1 aes128-ctr,aes192-ctr,aes256-ctr/' /etc/ssh/sshd_config

echo 'IgnoreRhosts yes' >> /etc/ssh/sshd_config

sed -ri 's/^(MACs) .*$/\1 hmac-sha2-512,hmac-sha2-256,hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com/' /etc/ssh/sshd_config

postconf -e 'smtpd_client_restrictions = permit_mynetworks,reject'

echo 'ALL: LOCAL
ALL: 192.168.0.0/16
ALL: 10.0.0.0/8' >> /etc/hosts.allow

echo 'ALL: ALL' >> /etc/hosts.deny

yum install -y authconfig-gtk

yum install -y sssd

# generate audit rules
cd /etc/audit/rules.d
echo '-e 2' > zzz_enable.rules
augenrules --load

# realmd
yum install -y realmd oddjob oddjob-mkhomedir sssd samba-common-tools dconf krb5-workstation

# splunk
#TODO
#yum install -y --nogpgcheck /var/rhel7repo/splunkforwarder*.rpm
#find /var/log -type d -exec chmod o+x '{}' \;
#find /var/log -type f -exec chmod o+r '{}' \;
#chgrp -R splunk /var/log/audit
#find /var/log/audit -type d -exec chmod 0750 '{}' \;
#find /var/log/audit -type f -exec chmod 0640 '{}' \;
#chgrp splunk /sbin/ausearch
#/opt/splunkforwarder/bin/splunk clone-prep-clear-config

# clear log files, sysprep
rm -f /var/log/audit/audit.log.*
rm -f /var/log/grubby_prune_debug
lastlog -C -u 0-65535
rm -f /var/log/sa/*
echo > /var/log/tuned/tuned.log
for i in /var/log/anaconda/*; do echo > $i; done
echo > /var/log/vmware-vgauthsvc.log.0
echo > /var/log/vmware-vmsvc.log
echo > /var/log/firewalld
echo > /var/log/yum.log
echo > /var/log/grubby
echo > /var/log/aide/aide.log
for i in /var/log/sssd/*; do echo > $i; done
rm -f /var/log/dmesg.old
for i in /var/log/boot.log-*; do rm -f $i; done
for i in /var/log/cron-*; do rm -f $i; done
for i in /var/log/maillog-*; do rm -f $i; done
for i in /var/log/messages-*; do rm -f $i; done
for i in /var/log/secure-*; do rm -f $i; done
for i in /var/log/btmp-*; do rm -f $i; done
echo > /var/log/dmesg
echo > /var/log/cron
echo > /var/log/maillog
echo > /var/log/secure
echo > /var/log/messages
echo > /var/log/audit/audit.log

# aide
aide --init
mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
