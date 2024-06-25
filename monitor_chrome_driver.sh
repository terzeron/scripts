#!/bin/bash

count=$(pgrep -c "chrome")
if [ "$count" -gt 5 ]; then
    send_msg_to_gmail.py -s "Monitoring chrome browser and driver" "Too many chrome or chromedriver processes ($count)"
fi

