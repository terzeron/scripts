#!/bin/bash

if [ "$1" != "" ]; then
    msg=$1
else
    msg=""
    while read line; do
        if [ "$msg" != "" ]; then
            msg="$msg\n$line"
        else
            msg="$line"
        fi
    done
fi

dir=$(dirname $0)
config_file="$dir/global_config.json"

line_access_token=$(jq -r ".line_access_token" < "$config_file")
receiver_line_id=$(jq -r ".receiver_line_id" < "$config_file")

line_push_url="https://api.line.me/v2/bot/message/push"
content_type_header="Content-Type: application/json"
auth_header="Authorization: Bearer $line_access_token"
payload='{ "to": "'$receiver_line_id'", "messages":[ { "type": "text", "text": "'$msg'" } ] }'

/usr/bin/curl -s -X POST -H "$content_type_header" -H "$auth_header" -d "$payload" "$line_push_url" > /dev/null
