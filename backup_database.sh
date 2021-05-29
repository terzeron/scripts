#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/Applications/MAMP/Library/bin

WORK_DIR=$HOME/workspace
BACKUP_DIR="$HOME/googledrive/googledrive/backup"

date_str=`date +"%y%m%d"`

# read config
credential_file=$(dirname $0)/backup_database.passwd.json
id=$(jq -r '.id' $credential_file)
passwd=$(jq -r '.passwd' $credential_file)
root_id=$(jq -r '.root_id' $credential_file)
root_passwd=$(jq -r '.root_passwd' $credential_file)

date
cd ${WORK_DIR}
pwd

function backup() {
    database=$1
    id=$2
    passwd=$3
    
    backup_file=${WORK_DIR}/${database}.db.sql.${date_str}.bz2
    echo "### making the backup file for $database database ###"
    mysqldump --no-tablespaces -h localhost -u $id -p$passwd $database | bzip2 --best > ${backup_file}
    echo "### moving the backup file '${backup_file}' to directory '${BACKUP_DIR}' ###"
    mv "${backup_file}" "${BACKUP_DIR}"
}

backup "terzeron" $id $passwd
#backup "confluence" $id $passwd
backup "rssextend" $id $passwd
backup "mysql" $root_id $root_passwd

date
