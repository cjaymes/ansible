#!/bin/bash

SHARE=/share/repo

declare -a REPOS
REPOS=(
    "base",
    "updates",
    "extras",
    "epel",
)

mkdir -p "$SHARE"
cd "$SHARE"
for d in ${REPOS[*]}; do
    reposync --plugins --gpgcheck --delete --downloadcomps --download-metadata --repoid=$d
    createrepo -v --update --groupfile comps.xml $d
done
