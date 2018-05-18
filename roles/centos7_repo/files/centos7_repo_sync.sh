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
cd "$SHARE"
for d in ${REPOS[*]}; do
    reposync --plugins --gpgcheck --delete --downloadcomps --download-metadata --repoid=$d
    createrepo --update --groupfile comps.xml $d
done
