#!/usr/bin/env python

import sys
import os
import re
from datetime import date, timedelta

st = {}
t = date.today()


def determine_date_range():
    s = "(?P<date>"
    for i in range(5):
        if s != "(":
            s += "|"
        dt = t - timedelta(i)
        s += str(dt)
    s += ")"
    return s


def count_error_log(file, date_range):
    #print(file)
    with open(file, "r") as f:
        st[file] = [0, 0, 0, 0, 0]
        for line in f:
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
                st[file][date_index] = st[file][date_index] + 1
    
    
def main():
    date_range = determine_date_range()
    #print(date_range)
    for path, dir, files in os.walk("/home/terzeron/workspace/fma/"):
        if "/_" not in path:
            for file in files:
                if file == "run.log":
                    #print(path, file)
                    count_error_log(os.path.join(path, file), date_range)

    for f in st:
        file = re.sub(r'(/home/terzeron/workspace/fma/|/run.log)', '', f)
        if st[f] == [0, 0, 0, 0, 0]:
            continue
        for v in st[f]:
            print("{:3d}".format(v), end='')
        category, feed = file.split('/')
        category = category[0] + re.sub(r'[aeiou_0-9]', '', category[1:])
        new_feed = ""
        for word in feed.split('_'):
            word = word[0] + re.sub(r'[aeiou0-9]', '', word[1:])
            if new_feed == "":
                new_feed = word
            else:
                new_feed += "_" + word
                
        print(" " + category + "/" + new_feed)


if __name__ == "__main__":
    sys.exit(main())
