#!/bin/bash

echo "-------------------------------------------------------------"
date

cd ~/workspace/fma
source ~/workspace/fma/.env

url="https://terzeron.com/crawler/js_rendering.html"
verification_msg="<div><span>Hello, World!</span></div>"
crawler.py --render-js=true "$url" | \
    grep "$verification_msg" > /dev/null || \
    send_msg_to_gmail.py "error in crawling by headless browser"

echo "-------------------------------------------------------------"
echo
