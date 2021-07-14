#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:$HOME/bin:$HOME/.pyenv/bin:$HOME/.pyenv/shims
export FM_HOME=$HOME/workspace/fma
export FM_PATH=$HOME/workspace/fm
export LOG_DIR=$HOME/logs

. ~/.bashrc
. $FM_PATH/bin/setup.sh

site_list=$*
for site in $site_list; do
    echo $site
    log=$LOG_DIR/check_manga_${site}.log

    cd $FM_HOME/$site
    check_manga_site.py > $log 2>&1 || \
        (echo "error in checking $site"; date; cat $log | send_msg_to_gmail.sh -s "error in checking $site")
done

