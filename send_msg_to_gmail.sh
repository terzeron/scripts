#!/bin/bash

subject="notification from terzeron.com"
if [ "$1" == "-s" ]; then
    subject="$2";
    shift
    shift
fi

if [ "$1" != "" ]; then
    msg=$1
    echo "$msg" | mutt -s "$subject" terzeron@gmail.com && \
    echo "sent a mail to gmail.com"
else
    cat - | mutt -s "$subject" terzeron@gmail.com && \
    echo "sent a mail to gmail.com"
fi

