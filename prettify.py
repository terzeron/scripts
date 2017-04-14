#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :


from bs4 import BeautifulSoup, Comment
import sys
import re

if __name__ == "__main__":
	html = open(sys.argv[1]).read()
	html = re.sub(r'alt="(.*)<br>(.*)"', r'alt="\1 \2"', html);
	html = re.sub(r'<br>', r'<br/>', html)
	html = re.sub(r'<\?xml[^>]+>', r'', html)
	html = re.sub(r'<!--.*-->', r'', html)
	soup = BeautifulSoup(html, 'html.parser')
	print(soup.prettify())
