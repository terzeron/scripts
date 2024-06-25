#!/bin/bash

echo "----------------------------------------------------------"
date

while (( $# )); do
    process_name="$1"
    shift
    
    if ! pgrep "$process_name" > /dev/null; then 
        echo "Error: can't find process" | send_msg_to_gmail.py -s "checking process '$process_name'"
    fi
done

echo "----------------------------------------------------------"
echo
