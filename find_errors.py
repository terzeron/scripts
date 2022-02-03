#!/usr/bin/env python

import sys
import os
import re
from datetime import datetime
from pathlib import Path
from datetime import date, timedelta


st = {}
t = date.today()


def determine_date_range() -> str:
    s = "(?P<date>"
    for i in range(5):
        if s != "(":
            s += "|"
        dt = t - timedelta(i)
        s += str(dt)
    s += ")"
    return s


def count_error_log(file: Path, date_range: str) -> None:
    state = 0
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if state == 0:
                m = re.search(r'\[' + current_date_str + ' \d\d:\d\d:\d\d[.,]\d+\]', line)
                if m:
                    state = 1
            elif state == 1:
                m = re.search(r'making feed file \'(?P<feed>[^\']+)\/[^/]+\.xml\'', line)
                if m:
                    feed = m.group("feed")
                    if feed not in st:
                        st[feed] = [0, 0, 0, 0, 0]
                
                m = re.search(r'\[' + date_range + ' .*\[ERROR\]', line)
                if m:
                    date = m.group("date")
                    if date == str(t):
                        date_index = 4
                    elif date == str(t - timedelta(1)):
                        date_index = 3
                    elif date == str(t - timedelta(2)):
                        date_index = 2
                    elif date == str(t - timedelta(3)):
                        date_index = 1
                    elif date == str(t - timedelta(4)):
                        date_index = 0
                    st[feed][date_index] = st[feed][date_index] + 1
    
    
def main():
    date_range = determine_date_range()
    #print(date_range)
    file = Path("/home/terzeron/workspace/fma/run.log")
    count_error_log(file, date_range)

    for f in st:
        file = re.sub(r'(/home/terzeron/workspace/fma/|/run.log)', '', str(f))
        if st[f] == [0, 0, 0, 0, 0]:
            continue
        for v in st[f]:
            print("{:3d}".format(v), end='')
        category, feed = file.split('/')
        #category = category[0] + re.sub(r'[aeiou_0-9]', '', category[1:])
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
