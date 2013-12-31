#!/bin/sh

file=$1
logfile="$file".log
transmission-cli --portmap --port 52970 "$file" > "$logfile" 2>&1 &
sleep 1
tail -f "$logfile" &
sleep 1
(while [ 1 ]; do grep Complete "$logfile" && break; sleep 2; done)
sleep 3
# kill transmission process
kill $(jobs -p)
# kill tail process
kill $(jobs -p)
rm "$logfile"
