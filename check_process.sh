#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:$HOME/bin:$HOME/.pyenv/bin:$HOME/.pyenv/shims
export LOG_DIR=$HOME/logs

while (( $# )); do
    process_name=$1
    shift

    pgrep $process_name || \
        (echo "Error: can't find process"; \
         echo;) | \
            send_msg_to_gmail.sh -s "checking process '$process_name'"
done
