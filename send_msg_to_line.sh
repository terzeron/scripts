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

/usr/bin/curl -s -X POST -H 'Content-Type:application/json' -H 'Authorization: Bearer gdrao6YPr50SCzwqb7By40yqwOotDdo9a/+nGYmFkL3xMUA1P3OPJO7aKlNTnN12tz0BzJ5C/TX+gTZiIUFeXIa8X1reFHNXPcJ/hlZysxTkBOkSzbEI/TUbBVDjves+lDqDwVicBisE3/MelN5QrAdB04t89/1O/w1cDnyilFU=' -d '{ "to": "U52aa71b262aa645ba5f3e4786949ef23", "messages":[ { "type": "text", "text": "'"$msg"'" }  ] }' https://api.line.me/v2/bot/message/push > /dev/null
