#!/bin/bash

subject="notification from terzeron.com"
if [ "$1" == "-s" ]; then
    subject="$2";
    shift
    shift
fi

if [ "$1" != "" ]; then
    msg=$1
    echo "$msg" | mailx -s "$subject" -r terzeron@terzeron.com terzeron@gmail.com 
else
    cat - | mailx -s "$subject" -r terzeron@terzeron.com terzeron@gmail.com 
fi

