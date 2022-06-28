#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

date_str=`date +"%y%m%d"`
WORK_DIR=$HOME/workspace
SRC_DIR=fma
backup_file=/mnt/data/nuc_backup/feedmaker.${date_str}.tar.bz2

date

cd $WORK_DIR

echo "### making the backup file ###"
tar cvfj $backup_file --exclude="*.log" --exclude="*.txt" $SRC_DIR > /dev/null

date
