#!/bin/bash

source /etc/repo.conf

mkdir -p "$SHARE"
REPO_FILE="$SHARE/$(hostname -s).repo"

# clear the file
echo > "$REPO_FILE"

cd "$SHARE"

for d in $REPOS; do
    echo Adding $d to $SHARE .repo file
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
