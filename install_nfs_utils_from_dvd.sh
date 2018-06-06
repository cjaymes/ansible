mount /dev/cdrom /mnt

cat > /etc/yum.repos.d/dvd.repo <<EOF
[InstallMedia]
name=Red Hat Enterprise Linux 7.5
mediaid=1521745267.626363
metadata_expire=-1
gpgcheck=1
cost=500
enabled=1
baseurl=file:///mnt/
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
EOF

rpmkeys --import /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

yum install -y nfs-utils

umount /mnt
