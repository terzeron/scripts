#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

date_str=`date +"%y%m%d"`

WORK_DIR=$HOME/Downloads
SRC_DIR=text
backup_file=/mnt/data2/nuc_backup/text.${date_str}.tar.bz2

date

cd ${WORK_DIR}
pwd

echo "### making the backup file ###"
tar cvfj ${backup_file} ${SRC_DIR}

date
