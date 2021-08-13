#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:$HOME/bin:$HOME/.pyenv/bin:$HOME/.pyenv/shims
export LOG_DIR=$HOME/logs

while (( $# )); do
    url=$1
    shift
    echo "url=$url"

    md5=$(echo $url | md5sum | cut -c-5)
    logfile=$LOG_DIR/check_terzeron_com_${md5}.log
    result=$((echo "$url"; curl "$url") > $logfile 2>&1)
    [ $? -eq 0 ] || \
        (echo "Error: can't access to $url"; \
         echo; \
         echo "----- logfile file ------";
         cat $logfile) | \
            send_msg_to_gmail.sh -s "checking $url"
done
