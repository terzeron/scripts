#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

WORK_DIR=$HOME/workspace
BACKUP_NAME=config
BACKUP_DIR="$HOME/googledrive/googledrive/backup"

date_str=`date +"%y%m%d"`
backup_file=${WORK_DIR}/${BACKUP_NAME}.${date_str}.tar.bz2

date

cd /

echo "### making the backup file ###"
tar cvfj ${backup_file} /etc > /dev/null

echo "### moving the backup file to storage ###"
sudo -u terzeron mv "${backup_file}" "${BACKUP_DIR}"

date
