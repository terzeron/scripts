#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

WORK_DIR=$HOME/workspace
BACKUP_NAME=config
BACKUP_DIR="$HOME/googledrive/googledrive/backup"

date_str=`date +"%y%m%d"`
backup_file=${WORK_DIR}/${BACKUP_NAME}.${date_str}.tar

date

for dir in /etc/apache2 /etc/php /etc/samba /etc/letsencrypt /etc/mysql /etc/ssh /opt/atlassian/confluence/conf /etc/libapache2-mod-jk; do
    cd ${dir}
    pwd

    [ -e "${backup_file}" ] && \
        (echo appending; tar --append --file=${backup_file} * > /dev/null) || \
    [ -e "${backup_file}" ] || \
        (echo creating; tar cvf ${backup_file} * > /dev/null)
done

echo "### compressing ###"
bzip2 ${backup_file}

echo "### moving the backup file to storage ###"
sudo -u terzeron mv "${backup_file}".bz2 "${BACKUP_DIR}"

date
