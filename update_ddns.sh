#!/bin/bash

echo "----------------------------------------------------"
date

# read config
credential_file=$(dirname "$0")/update_ddns.passwd.json
id=$(jq -r '.id' "$credential_file")
passwd=$(jq -r '.password' "$credential_file")

# host list
host_list="terzeron.com mail.terzeron.com"
host_param_str=""
for host in $host_list; do
    if [ "$host_param_str" == "" ]; then
        host_param_str="?host[$host]"
    else
        host_param_str="${host_param_str}&host[$host]"
    fi
done

cd "$HOME/logs" || exit
current_logfile="myip.log.current"
previous_logfile="myip.log"
curl -s https://ipinfo.io/ip > $current_logfile
if diff "$current_logfile" "$previous_logfile" > /dev/null; then
    echo "no change"
else
    echo "updating"
    curl -u "$id:$passwd" -g "http://dyna.dnsever.com/update.php${host_param_str}"
    mv "$current_logfile" "$previous_logfile"
fi

echo "----------------------------------------------------"
echo
