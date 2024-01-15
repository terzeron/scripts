#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:$HOME/bin:$HOME/.pyenv/bin:$HOME/.pyenv/shims
export LOG_DIR=$HOME/logs

while (( $# )); do
    url="$1"
    shift
    echo "url=$url"

    md5=$(echo "$url" | md5sum | cut -c-5)
    logfile=$LOG_DIR/check_terzeron_com_${md5}.log
    if !(echo "$url"; curl --connect-timeout 30 --max-time 60 -vsLI -w "리다이렉트 시간:\t%{time_redirect}\nDNS lookp 시간:\t\t%{time_namelookup}\n연결 시간:\t\t%{time_connect}\n애플리케이션 연결 시간: %{time_appconnect}\n전송 시작 시간:\t\t%{time_pretransfer}\n첫 바이트 수신 시간:\t%{time_starttransfer}\n총 시간:\t\t%{time_total}\n" "$url") > "$logfile" 2>&1; then
        ( 
            echo "Error: can't access to $url"
            echo
            echo "----- logfile file ------"
            cat "$logfile"
        ) | send_msg_to_gmail.py -s "checking $url"
    else
        cat "$logfile" | grep "^HTTP" | awk -F" " '$2 < 200 || (400 <= $2 && $2 < 600) { print "Error: "$0; }' | grep "Error:" > /dev/null && cat "$logfile" | send_msg_to_gmail.py -s "checking $url" || echo "Success"
    fi
done
