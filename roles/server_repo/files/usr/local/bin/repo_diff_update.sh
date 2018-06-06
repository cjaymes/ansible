#!/bin/bash

source /etc/repo.conf

REPONAME=`basename "$SHARE"`

[ -n "$1" ] && echo "Usage: $0 ${REPONAME}_yyyymmdd.tgz" && exit 1

echo Extracting $1 into $SHARE
tar --extract --gzip --verbose --file="$1" --directory="$SHARE"

cd "$SHARE"

for d in $REPOS; do
    echo Updating metadata in $SHARE/$d
    if [ -f "$SHARE/$d/comps.xml" ]; then
        createrepo --update --groupfile comps.xml $d
    else
        createrepo --update $d
    fi
    [ 0 != $? ] && echo "Got error $?" && exit 1
done

echo Fixing permissions in $SHARE
find $REPOPATH -type f -exec chmod -v a+r '{}' \;
find $REPOPATH -type d -exec chmod -v 0755 '{}' \;
