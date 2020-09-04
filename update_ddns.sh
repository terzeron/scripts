#!/bin/bash

# read config
id=$(jq -r '.id' update_ddns.sh.passwd)
passwd=$(jq -r '.password' update_ddns.sh.passwd)

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

cd $HOME/logs
current_logfile="myip.log.current"
previous_logfile="myip.log"
curl -s https://ipinfo.io/ip > $current_logfile
diff $current_logfile $previous_logfile || \
    ( \
      echo updating; \
      curl -u $id:$passwd -g "http://dyna.dnsever.com/update.php${host_param_str}"; \
      mv $current_logfile $previous_logfile; \
    )
