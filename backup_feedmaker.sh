#!/bin/bash

HOME=/home/terzeron
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

date_str=`date +"%y%m%d"`
WORK_DIR=$HOME/workspace
SRC_DIR=fma
backup_dir=/mnt/data/backup
backup_file=feedmaker.${date_str}.tar.bz2
if [ -d "$backup_dir" ]; then
    backup_path="$backup_dir/$backup_file"
else
    backup_path="$HOME/$backup_file"
fi

date

cd $WORK_DIR

echo "### making the backup file ###"
tar cvfj "$backup_path" --exclude="*.log" --exclude="*.txt" "$SRC_DIR" > /dev/null

date
