REPOS="base updates extras epel"
cd /share/CentOS/7
for d in $REPOS; do
    reposync --plugins --gpgcheck --delete --downloadcomps --download-metadata --repoid=$d
    createrepo -v --update $d
done
