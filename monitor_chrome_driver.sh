#!/bin/bash

count=$(ps aux | egrep "(chromedriver|google-chrome)" | grep -v grep | wc -l)
if [ "$count" -gt 5 ]; then
    send_msg_to_line.sh "Too many chrome driver processes ($count)"
fi

