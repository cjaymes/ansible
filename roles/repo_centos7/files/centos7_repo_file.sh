#!/bin/bash

SHARE=/share/repo

declare -a REPOS
REPOS=(
    "base"
    "updates"
    "extras"
    "epel"
)
DISABLED_REPOS=(
    "centosplus"
    "cr"
    "base-debuginfo"
    "fasttrack"
    "base-source"
    "updates-source"
    "extras-source"
    "centosplus-source"
    "epel-debuginfo"
    "epel-source"
    "epel-testing"
    "epel-testing-debuginfo"
    "epel-testing-source"
)

mkdir -p "$SHARE"
REPO_FILE="$SHARE/$(hostname -s).repo"
echo > "$REPO_FILE"
cd "$SHARE"
for d in ${REPOS[*]}; do
    cat >> "$REPO_FILE" <<"EOF"
[$d]
name = $d
baseurl = file://$SHARE/$d
enabled = 1
keepcache = 0
gpgcheck = 1
repo_gpgcheck = 0

EOF
done
