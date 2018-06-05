#!/bin/sh
source /etc/repo.conf

REPONAME=$(basename "$SHARE")

txt=~/${REPONAME}_$(date '+%Y%m%d').txt
tgz=~/${REPONAME}_$(date '+%Y%m%d').tgz

echo Finding packages modified in the last 45 days
files=$(find $SHARE -mtime -45 -printf '%P' | sort)

echo Fixing permissions in $SHARE
find $SHARE -type f -exec chmod -v a+r '{}' \;
find $SHARE -type d -exec chmod -v 0755 '{}' \;

echo Packaging patches into $tgz
tar --create --gzip --verbose --file="$tgz"  $files
