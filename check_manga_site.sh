#!/bin/bash

echo "----------------------------------------------------------------"
date

. ~/workspace/fma/.env

site_list=$*
for site in $site_list; do
    echo "$site"
    log=$FM_LOG_DIR/check_manga_${site}.log
    searchresult=$FM_LOG_DIR/search_manga_${site}.result.log
    searcherror=$FM_LOG_DIR/search_manga_${site}.error.log
    
    cd "$FM_WORK_DIR"/"$site" || exit
    
    if ! check_manga_site.py > "$log" 2>&1; then
        new_number=$(grep "New number: " "$log" | sed -E 's/New number: ([0-9][0-9]*)/\1/')
        echo "new_number=$new_number"
        if [ "$new_number" != "" ]; then
            echo "updating to $new_number"
            update_manga_site.py "$new_number" >> "$log" 2>&1
            echo "error in checking $site"
            date
            (echo "error in checking $site"; cat "$log") | send_msg_to_gmail.py -s "error in checking $site"
        fi
    fi

    if [ "${site%"${site#?}"}" != "_" ]; then
        keyword=$(jq -r .keyword < site_config.json)
        search_manga_site.py -s "$site" "$keyword" > "$searchresult" 2> "$searcherror"
        num_lines=$(wc -l < "$searchresult")
        if [ "$num_lines" -lt 1 ]; then
            echo "error in searching '$keyword' in $site"
            date
            (echo "error in searching '$keyword' in $site"; cat "$searcherror") | send_msg_to_gmail.py -s "error in search $site"
        fi
    fi
    sleep 5
done

echo "----------------------------------------------------------------"
echo
