#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

date_str=`date +"%y%m%d"`
WORK_DIR=$HOME
SRC_DIR=public_html
backup_file=/mnt/data/nuc_backup/publichtml.${date_str}.tar.bz2

date

cd $WORK_DIR

echo "### making the backup file ###"
tar cvfj $backup_file --exclude="public_html/photo/*" --exclude="public_html/xml/*" --exclude="public_html/rss_extend/logs/*" --exclude="public_html/rss_extend/cache/*" --exclude="public_html/node_modules" --exclude="public_html/*/node_modules" --exclude="public_html/*/*/node_modules" $SRC_DIR > /dev/null

date
