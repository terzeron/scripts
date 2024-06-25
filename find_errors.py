#!/usr/bin/env python

import sys
import re
import os
from glob import glob
from datetime import date, timedelta
from typing import Dict, List
from pathlib import Path


st: Dict[str, List[int]] = {}
today = date.today()


def determine_date_range_pattern(num_days: int) -> str:
    s = "(?P<date>"
    for i in range(num_days):
        if s != "(?P<date>":
            s += "|"
        dt = today - timedelta(i)
        s += str(dt)
    s += ")"
    return s


def count_error_log(file: Path, date_range: str, num_days) -> None:
    state = 0

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if state == 0:
                m = re.search(r'making feed file \'(?P<feed>[^\']+)\/[^/]+\.xml\'', line)
                if m:
                    feed = m.group("feed")
                    if feed not in st:
                        st[feed] = [0] * num_days
                    state = 1
            elif state == 1:
                m = re.search(r'\[' + date_range + ' .*\[ERROR\]', line)
                if m:
                    dt = m.group("date")
                    for i in range(num_days):
                        if dt == str(today - timedelta(i)):
                            dt_index = num_days - i - 1
                            break
                    st[feed][dt_index] = st[feed][dt_index] + 1
                    state = 0
                m = re.search(r'Elapsed time', line)
                if m:
                    state = 0


def main():
    num_days = 7
    date_range = determine_date_range_pattern(num_days)
    #print(date_range)
    for file in glob(os.environ["FM_WORK_DIR"] + "/run.log*"):
        count_error_log(file, date_range, num_days)
        
    for feed_name in st:
        feed_name = re.sub(r'(/home/terzeron/workspace/fma/|/run.log)', '', str(feed_name))
        if st[feed_name] == [0] * num_days:
            continue
        for v in st[feed_name]:
            print("{:3d}".format(v), end='')
        category, feed = feed_name.split('/')
        category = category[0] + category[1:]
        new_feed = ""
        for word in feed.split('_'):
            #word = word[0] + re.sub(r'[aeiou0-9]', '', word[1:])
            word = word[0] + word[1:]
            if new_feed == "":
                new_feed = word
            else:
                new_feed += "_" + word

        print(" " + category + "/" + new_feed)


if __name__ == "__main__":
    sys.exit(main())
