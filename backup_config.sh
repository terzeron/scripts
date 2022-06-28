#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

date_str=`date +"%y%m%d"`
WORK_DIR=/
SRC_DIR=etc
backup_file=/mnt/data/nuc_backup/config.${date_str}.tar.bz2

date

cd $WORK_DIR

echo "### making the backup file ###"
tar cvfj $backup_file $SRC_DIR > /dev/null

date
