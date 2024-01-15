#!/bin/bash

HOME=/home/terzeron
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/Applications/MAMP/Library/bin:/snap/bin

date_str=`date +"%y%m%d"`
WORK_DIR=$HOME/workspace

date

cd ${WORK_DIR}

function backup() {
    deployment="$1"
    namespace="$2"

    kubens "$namespace"
    deployment_description=$(kubectl get deployment "$deployment" -o yaml)
    service=$(echo "$deployment_description" | yq eval '.spec.template.spec.containers[].env[] | select(.name == "MARIADB_HOST").value')
    host_ip=$(kubectl get service "$service" -o yaml | yq eval '.spec.clusterIP')
    port=$(echo "$deployment_description" | yq eval '.spec.template.spec.containers[].env[] | select(.name == "MARIADB_PORT_NUMBER").value')
    database=$(echo "$deployment_description" | yq eval '.spec.template.spec.containers[].env[] | select(.name == "WORDPRESS_DATABASE_NAME").value')
    user=$(echo "$deployment_description" | yq eval '.spec.template.spec.containers[].env[] | select(.name == "WORDPRESS_DATABASE_USER").value')
    passwd_secret_key=$(echo "$deployment_description" | yq eval '.spec.template.spec.containers[].env[] | select(.name == "WORDPRESS_DATABASE_PASSWORD").valueFrom.secretKeyRef.name')
    user_passwd=$(kubectl get secret "$passwd_secret_key" -o yaml | yq '.data.mariadb-password' | base64 --decode)
    root_passwd=$(kubectl get secret "$passwd_secret_key" -o yaml | yq '.data.mariadb-root-password' | base64 --decode)
    
    backup_dir=/mnt/data/backup
    backup_file=${database}.db.sql.${date_str}.bz2
    if [ -d "$backup_dir" ]; then
        backup_path="$backup_dir/$backup_file"
    else
        backup_path="$HOME/$backup_file"
    fi

    echo "### making the backup file for '$database' database ###"
    mysqldump --no-tablespaces -h "$host_ip" -P "$port" -u "$user" "$database" -p"$user_passwd" | bzip2 --best > ${backup_path}
}

backup "wp-wordpress" "blog"

date
