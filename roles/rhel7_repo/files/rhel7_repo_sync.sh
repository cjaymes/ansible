#!/bin/bash

SHARE=/share/repo

declare -a REPOS
REPOS=(
    "rhel-7-server-extras-rpms"
    "rhel-7-server-rh-common-rpms"
    "rhel-ha-for-rhel-7-server-rpms"
    "rhel-7-server-ansible-2.5-rpms"
    "rhel-7-server-devtools-rpms"
    "rhel-7-server-supplementary-rpms"
    "rhel-7-server-rt-rpms"
    "rhel-7-server-optional-rpms"
    "rhel-7-server-rpms",
)
# "rhel-7-server-dotnet-debug-rpms",
# "rhel-ha-for-rhel-7-server-beta-source-rpms",
# "rhel-7-server-v2vwin-1-debug-rpms",
# "rhel-7-server-insights-3-debug-rpms",
# "rhel-7-server-satellite-maintenance-6-debug-rpms",
# "rhel-7-server-eus-satellite-tools-6.3-puppet4-debug-rpms",
# "rhel-7-server-eus-satellite-tools-6.3-debug-rpms",
# "rhel-atomic-7-cdk-3.0-source-rpms",
# "rhel-rs-for-rhel-7-server-fastrack-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.3-puppet4-debug-rpms",
# "rhel-7-server-openstack-9-tools-rpms",
# "rhel-7-server-ansible-2-rpms",
# "rhel-7-server-openstack-11-tools-debug-rpms",
# "rhel-atomic-7-cdk-2.3-rpms",
# "rhel-server-rhscl-7-eus-source-rpms",
# "rhel-7-server-eus-rh-common-rpms",
# "rhel-7-server-satellite-tools-6-beta-rpms",
# "rhel-ha-for-rhel-7-server-fastrack-rpms",
# "rhel-rs-for-rhel-7-server-eus-rpms",
# "rhel-7-server-rhceph-2-tools-rpms",
# "rhel-7-server-eus-debug-rpms",
# "rhel-7-server-devtools-beta-source-rpms",
# "rhel-7-server-ansible-2-source-rpms",
# "rhel-sap-for-rhel-7-server-e4s-rpms",
# "rhel-atomic-host-beta-debug-rpms",
# "rhel-sap-for-rhel-7-server-e4s-source-rpms",
# "rhel-7-server-openstack-12-tools-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.3-rpms",
# "rhel-server-rhscl-7-beta-rpms",
# "rhel-7-server-satellite-tools-6.1-debug-rpms",
# "rhel-server-rhscl-7-beta-source-rpms",
# "rhel-7-server-e4s-satellite-tools-6.3-puppet4-source-rpms",
# "rhel-7-server-devtools-beta-rpms",
# "rhel-7-server-eus-satellite-tools-6.1-debug-rpms",
# "rhel-7-server-eus-source-rpms",
# "rhel-7-server-beta-source-rpms",
# "rhel-7-server-devtools-source-rpms",
# "rhel-7-server-e4s-satellite-tools-6.3-puppet4-rpms",
# "rhel-sap-hana-for-rhel-7-server-beta-rpms",
# "rhel-7-server-satellite-tools-6-puppet-upgrade-beta-rpms",
# "rhel-ha-for-rhel-7-server-eus-debug-rpms",
# "rhel-rs-for-rhel-7-server-debug-rpms",
# "rhel-7-server-optional-beta-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.3-debug-rpms",
# "rhel-sap-hana-for-rhel-7-server-eus-debug-rpms",
# "rhel-server-rhscl-7-beta-debug-rpms",
# "rhel-ha-for-rhel-7-server-e4s-source-rpms",
# "rhel-7-server-optional-fastrack-debug-rpms",
# "rhel-sap-hana-for-rhel-7-server-rpms",
# "rhel-7-server-satellite-tools-6.2-source-rpms",
# "rhel-7-server-satellite-tools-6.3-puppet4-rpms",
# "rhel-7-server-e4s-source-rpms",
# "rhel-rs-for-rhel-7-server-eus-source-rpms",
# "rhel-7-server-eus-rh-common-debug-rpms",
# "rhel-atomic-7-cdk-3.2-rpms",
# "rhel-ha-for-rhel-7-server-eus-rpms",
# "rhel-rs-for-rhel-7-server-source-rpms",
# "rhel-7-server-openstack-12-tools-rpms",
# "rhel-7-server-eus-satellite-tools-6.1-source-rpms",
# "rhel-7-server-rhceph-1.3-tools-source-rpms",
# "rhel-7-server-rt-beta-debug-rpms",
# "rhel-7-server-eus-satellite-tools-6.3-puppet4-rpms",
# "rhel-7-server-satellite-tools-6-beta-source-rpms",
# "rhel-7-server-openstack-10-tools-debug-rpms",
# "rhel-7-server-eus-rh-common-source-rpms",
# "rhel-7-server-eus-rpms",
# "rhel-atomic-7-cdk-3.1-debug-rpms",
# "rhel-7-server-optional-fastrack-source-rpms",
# "rhel-7-server-e4s-debug-rpms",
# "rhel-7-server-thirdparty-oracle-java-beta-source-rpms",
# "rhel-7-server-rt-beta-source-rpms",
# "rhel-atomic-host-debug-rpms",
# "rhel-7-server-optional-debug-rpms",
# "rhel-ha-for-rhel-7-server-e4s-debug-rpms",
# "rhel-ha-for-rhel-7-server-source-rpms",
# "rhel-7-server-supplementary-beta-source-rpms",
# "rhel-7-server-rhceph-1.3-tools-debug-rpms",
# "rhel-7-server-openstack-10-tools-rpms",
# "rhel-ha-for-rhel-7-server-eus-source-rpms",
# "rhel-server-rhscl-7-eus-debug-rpms",
# "rhel-7-server-eus-satellite-tools-6.2-source-rpms",
# "rhel-atomic-7-cdk-3.0-beta-debug-rpms",
# "rhel-atomic-7-cdk-2.4-debug-rpms",
# "rhel-7-server-ansible-2.4-debug-rpms",
# "rhel-sjis-for-rhel-7-server-eus-source-rpms",
# "rhel-7-server-eus-supplementary-rpms",
# "rhel-sap-for-rhel-7-server-eus-rpms",
# "rhel-7-server-extras-beta-debug-rpms",
# "rhel-server-rhscl-7-rpms",
# "rhel-7-server-rt-beta-rpms",
# "rhel-sap-hana-for-rhel-7-server-beta-source-rpms",
# "rhel-7-server-eus-satellite-tools-6.2-debug-rpms",
# "rhel-7-server-rhn-tools-rpms",
# "rhel-atomic-7-cdk-3.1-rpms",
# "rhel-rs-for-rhel-7-server-fastrack-rpms",
# "rhel-atomic-7-cdk-3.0-rpms",
# "rhel-atomic-7-cdk-2.3-debug-rpms",
# "rhel-7-server-e4s-optional-source-rpms",
# "rhel-7-server-thirdparty-oracle-java-rpms",
# "rhel-atomic-7-cdk-3.2-source-rpms",
# "rhel-7-server-fastrack-rpms",
# "rhel-7-server-satellite-tools-6.2-rpms",
# "rhel-7-server-openstack-9-tools-source-rpms",
# "rhel-sap-for-rhel-7-server-eus-debug-rpms",
# "rhel-7-server-eus-satellite-tools-6.2-rpms",
# "rhel-7-server-dotnet-rpms",
# "rhel-7-server-rh-common-debug-rpms",
# "rhel-7-server-thirdparty-oracle-java-beta-rpms",
# "rhel-7-server-optional-fastrack-rpms",
# "rhel-7-server-e4s-rpms",
# "rhel-7-server-satellite-tools-6-puppet-upgrade-beta-source-rpms",
# "rhel-atomic-host-rpms",
# "rhel-7-server-ansible-2.5-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.3-source-rpms",
# "rhel-7-server-eus-rhn-tools-source-rpms",
# "rhel-7-server-rhn-tools-beta-rpms",
# "rhel-7-server-rt-debug-rpms",
# "rhel-7-server-e4s-optional-debug-rpms",
# "rhel-7-server-source-rpms",
# "rhel-7-server-extras-source-rpms",
# "rhel-7-server-openstack-7.0-tools-debug-rpms",
# "rhel-7-server-rh-common-beta-rpms",
# "rhel-sap-hana-for-rhel-7-server-eus-rpms",
# "rhel-atomic-host-source-rpms",
# "rhel-atomic-7-cdk-2.4-rpms",
# "rhel-7-server-openstack-10-tools-source-rpms",
# "rhel-atomic-host-beta-rpms",
# "rhel-7-server-supplementary-debug-rpms",
# "rhel-sap-for-rhel-7-server-e4s-debug-rpms",
# "rhel-rs-for-rhel-7-server-beta-debug-rpms",
# "rhel-7-server-fastrack-debug-rpms",
# "rhel-rs-for-rhel-7-server-rpms",
# "rhel-7-server-satellite-tools-6.2-debug-rpms",
# "rhel-atomic-host-beta-source-rpms",
# "rhel-7-server-eus-satellite-tools-6.3-source-rpms",
# "rhel-7-server-rhn-tools-beta-debug-rpms",
# "rhel-7-server-insights-3-rpms",
# "rhel-7-server-openstack-8-tools-source-rpms",
# "rhel-7-server-eus-supplementary-source-rpms",
# "rhel-7-server-satellite-maintenance-6-rpms",
# "rhel-7-server-openstack-9-tools-debug-rpms",
# "rhel-atomic-7-cdk-3.2-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.2-source-rpms",
# "rhel-7-server-eus-satellite-tools-6.1-rpms",
# "rhel-7-server-v2vwin-1-rpms",
# "rhel-7-server-extras-beta-source-rpms",
# "rhel-atomic-7-cdk-2.4-source-rpms",
# "rhel-7-server-dotnet-beta-debug-rpms",
# "rhel-rs-for-rhel-7-server-eus-debug-rpms",
# "rhel-7-server-openstack-11-tools-rpms",
# "rhel-7-server-rhceph-2-tools-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.2-rpms",
# "rhel-sap-hana-for-rhel-7-server-eus-source-rpms",
# "rhel-7-server-eus-optional-rpms",
# "rhel-server-rhscl-7-debug-rpms",
# "rh-gluster-3-client-for-rhel-7-server-debug-rpms",
# "rhel-7-server-insights-3-source-rpms",
# "rhel-atomic-7-cdk-3.3-debug-rpms",
# "rhel-7-server-v2vwin-1-source-rpms",
# "rhel-7-server-extras-debug-rpms",
# "rhel-7-server-openstack-12-tools-source-rpms",
# "rhel-server-rhscl-7-source-rpms",
# "rhel-7-server-e4s-optional-rpms",
# "rhel-7-server-ansible-2.4-rpms",
# "rhel-7-server-rhn-tools-beta-source-rpms",
# "rhel-7-server-satellite-tools-6-puppet-upgrade-beta-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.2-debug-rpms",
# "rhel-7-server-dotnet-beta-rpms",
# "rhel-7-server-satellite-tools-6.3-rpms",
# "rhel-7-server-satellite-tools-6.1-rpms",
# "rhel-7-server-satellite-tools-6.1-source-rpms",
# "rhel-7-server-eus-optional-source-rpms",
# "rhel-atomic-7-cdk-3.0-beta-source-rpms",
# "rhel-atomic-7-cdk-3.1-source-rpms",
# "rhel-ha-for-rhel-7-server-fastrack-debug-rpms",
# "rhel-7-server-rh-common-beta-source-rpms",
# "rhel-7-server-thirdparty-oracle-java-source-rpms",
# "rhel-7-server-satellite-maintenance-6-source-rpms",
# "rhel-7-server-eus-supplementary-debuginfo",
# "rhel-7-server-supplementary-beta-rpms",
# "rhel-sap-hana-for-rhel-7-server-source-rpms",
# "rhel-7-server-eus-thirdparty-oracle-java-rpms",
# "rhel-atomic-7-cdk-2.2-rpms",
# "rhel-sap-for-rhel-7-server-eus-source-rpms",
# "rhel-7-server-rh-common-source-rpms",
# "rhel-7-server-e4s-satellite-tools-6.1-debug-rpms",
# "rhel-7-server-rhceph-2-tools-source-rpms",
# "rhel-atomic-7-cdk-3.3-rpms",
# "rhel-rs-for-rhel-7-server-beta-source-rpms",
# "rhel-7-server-rhn-tools-debug-rpms",
# "rhel-7-server-eus-rhn-tools-rpms",
# "rhel-7-server-ansible-2-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.1-rpms",
# "rhel-7-server-devtools-beta-debug-rpms",
# "rhel-rs-for-rhel-7-server-fastrack-source-rpms",
# "rhel-7-server-ansible-2.5-source-rpms",
# "rh-gluster-3-client-for-rhel-7-server-rpms",
# "rhel-7-server-beta-rpms",
# "rhel-7-server-debug-rpms",
# "rhel-7-server-optional-beta-source-rpms",
# "rhel-server-rhscl-7-eus-rpms",
# "rhel-7-server-supplementary-beta-debug-rpms",
# "rh-gluster-3-client-for-rhel-7-server-source-rpms",
# "rhel-7-server-satellite-tools-6.3-debug-rpms",
# "rhel-7-server-rt-source-rpms",
# "rhel-atomic-7-cdk-3.3-source-rpms",
# "rhel-7-server-eus-satellite-tools-6.3-rpms",
# "rhel-7-server-satellite-tools-6.3-puppet4-debug-rpms",
# "rhel-sap-hana-for-rhel-7-server-debug-rpms",
# "rhel-7-server-satellite-tools-6.3-source-rpms",
# "rhel-7-server-eus-optional-debug-rpms",
# "rhel-ha-for-rhel-7-server-beta-rpms",
# "rhel-7-server-rhn-tools-source-rpms",
# "rhel-ha-for-rhel-7-server-beta-debug-rpms",
# "rhel-7-server-rh-common-beta-debug-rpms",
# "rhel-7-server-openstack-8-tools-rpms",
# "rhel-7-server-rhceph-1.3-tools-rpms",
# "rhel-7-server-satellite-tools-6.3-puppet4-source-rpms",
# "rhel-7-server-openstack-7.0-tools-rpms",
# "rhel-7-server-satellite-tools-6-beta-debug-rpms",
# "rhel-sjis-for-rhel-7-server-eus-debug-rpms",
# "rhel-7-server-dotnet-beta-source-rpms",
# "rhel-atomic-7-cdk-2.2-source-rpms",
# "rhel-7-server-openstack-8-tools-debug-rpms",
# "rhel-ha-for-rhel-7-server-e4s-rpms",
# "rhel-7-server-extras-beta-rpms",
# "rhel-7-server-dotnet-source-rpms",
# "rhel-atomic-7-cdk-3.0-debug-rpms",
# "rhel-7-server-e4s-satellite-tools-6.1-source-rpms",
# "rhel-ha-for-rhel-7-server-fastrack-source-rpms",
# "rhel-ha-for-rhel-7-server-debug-rpms",
# "rhel-atomic-7-cdk-2.3-source-rpms",
# "rhel-7-server-fastrack-source-rpms",
# "rhel-7-server-eus-thirdparty-oracle-java-source-rpms",
# "rhel-7-server-openstack-11-tools-source-rpms",
# "rhel-sap-hana-for-rhel-7-server-beta-debug-rpms",
# "rhel-7-server-eus-rhn-tools-debug-rpms",
# "rhel-atomic-7-cdk-2.2-debug-rpms",
# "rhel-7-server-beta-debug-rpms",
# "rhel-7-server-ansible-2.4-source-rpms",
# "rhel-rs-for-rhel-7-server-beta-rpms",
# "rhel-7-server-optional-beta-rpms",
# "rhel-7-server-supplementary-source-rpms",
# "rhel-sjis-for-rhel-7-server-eus-rpms",
# "rhel-7-server-devtools-debug-rpms",
# "rhel-7-server-optional-source-rpms",
# "rhel-7-server-openstack-7.0-tools-source-rpms",
# "rhel-7-server-eus-satellite-tools-6.3-puppet4-source-rpms",

mkdir -p "$SHARE"
cd "$SHARE"
for d in ${REPOS[*]}; do
    reposync --plugins --gpgcheck --delete --downloadcomps --download-metadata --repoid=$d
    createrepo -v --update --groupfile comps.xml $d
done
