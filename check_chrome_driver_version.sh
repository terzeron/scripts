#!/bin/bash

export PATH=/usr/bin:/home/terzeron/bin

driver_version=$(chromedriver --version | awk -F "[ \.]" '{print $2}')
browser_version=$(google-chrome-stable --version | awk -F "[ \.]" '{print $3}')

if [ "$driver_version" != "$browser_version" ]; then
    (echo "chromedriver: $driver_version"; echo "google-chrome-stable: $browser_version") | \
        send_msg_to_gmail.py -s "chrome driver version mismatch" 
fi
