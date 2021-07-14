#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:$HOME/bin:$HOME/.pyenv/bin:$HOME/.pyenv/shims
export LOG_DIR=$HOME/logs

while (( $# )); do
    url=$1
    shift
    validation_msg=$1
    shift

    log=$LOG_DIR/result.log
    result=$(curl -s "$url")
    echo "$result" | grep "$validation_msg" > $log || \
        (echo "Error: can't access to $url"; \
         echo; \
         echo "------ result ------"; \
         echo "$result"; \
         echo; \
         echo "----- log file ------";
         cat $log;) | \
            send_msg_to_gmail.sh -s "checking $url"
done
