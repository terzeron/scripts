#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/Applications/MAMP/Library/bin

date_str=`date +"%y%m%d"`
WORK_DIR=$HOME/workspace

# read config
credential_file=$(dirname $0)/backup_database.passwd.json
id=$(jq -r '.id' $credential_file)
passwd=$(jq -r '.passwd' $credential_file)
root_id=$(jq -r '.root_id' $credential_file)
root_passwd=$(jq -r '.root_passwd' $credential_file)

date

cd ${WORK_DIR}

function backup() {
    database=$1
    id=$2
    passwd=$3
    
    backup_file=/mnt/data/nuc_backup/${database}.db.sql.${date_str}.bz2
    echo "### making the backup file for $database database ###"
    mysqldump --no-tablespaces -h localhost -u $id -p$passwd $database | bzip2 --best > ${backup_file}
}

backup "terzeron" $id $passwd
backup "rssextend" $id $passwd
backup "mysql" $root_id $root_passwd

date
