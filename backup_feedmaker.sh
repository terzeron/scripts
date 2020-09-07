#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

WORK_DIR=$HOME/workspace
SRC_DIR=fma
BACKUP_NAME=feedmaker
BACKUP_DIR="$HOME/googledrive/googledrive/backup"

date_str=`date +"%y%m%d"`
backup_file=${WORK_DIR}/${BACKUP_NAME}.${date_str}.tar.bz2

date
cd ${WORK_DIR}
pwd

echo "### making the backup file ###"
tar cvfj ${backup_file} --exclude="*.log" --exclude="*.txt" ${SRC_DIR}
echo "### moving the backup file to storage ###"
mv "${backup_file}" "${BACKUP_DIR}"

date
