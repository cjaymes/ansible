#!/bin/bash

source /etc/repo.conf

mkdir -p "$SHARE"
cd "$SHARE"
for d in ${REPOS[*]}; do
    echo Synchronizing repo $d with $SHARE/$d
    reposync --plugins --gpgcheck --delete --downloadcomps --download-metadata --repoid=$d
    [ 0 != $? ] && echo "Got error $?" && exit 1

    echo Updating metadata in $SHARE/$d
    createrepo --update --groupfile comps.xml $d
    [ 0 != $? ] && echo "Got error $?" && exit 1
done

echo Fixing permissions in $SHARE
find $REPOPATH -type f -exec chmod -v a+r '{}' \;
find $REPOPATH -type d -exec chmod -v 0755 '{}' \;
