#!/usr/bin/env python

import os
import sys
import json
import re
import urllib
import logging
import logging.config
from typing import Dict, Tuple, List
from bs4 import BeautifulSoup
from crawler import Crawler, Method
from feed_maker_util import URL, HTMLExtractor


logging.config.fileConfig(os.environ["FEED_MAKER_HOME_DIR"] + "/bin/logging.conf")
LOGGER = logging.getLogger()


def print_content(site_name: str, result_list: List[Tuple[str, str]]) -> None:
    print("--------------------- %s -------------------------" % site_name)
    for title, link in result_list:
        print("%s\t%s" % (title, link))
    print("-------------------------------------------------------")


def get_data_from_site(config, url_postfix, method=Method.GET, headers={}, data={}) -> str:
    url_prefix = URL.get_url_scheme(config["url"]) + "://" + URL.get_url_domain(config["url"])
    encoding = config["encoding"] if "encoding" in config else None
    render_js = config["render_js"] if "render_js" in config else False
    c = Crawler(render_js=render_js, method=method, headers=headers, encoding=encoding)
    url = url_prefix + url_postfix
    response = c.run(url=url, data=data)
    return response


def extract_sub_content_by_attrs(search_url: str, content: str, attrs: Dict[str, str]) -> List[Tuple[str, str]]:
    #LOGGER.debug("content=%s", content)
    soup = BeautifulSoup(content, "html.parser")
    for key in attrs.keys():
        if key in ("id", "class"):
            content = soup.find_all(attrs={key: attrs[key]})
        elif key == "path":
            content = HTMLExtractor.get_node_with_path(soup.body, attrs[key])

        result_list = []
        for e in content:
            title = ""
            link = ""
            #LOGGER.debug(e)
            m = re.search(r'<a[^>]*href="(?P<link>[^"]+)"[^>]*>', str(e))
            if m:
                if m.group("link").startswith("http"):
                    link = m.group("link")
                else:
                    link = URL.concatenate_url(search_url, m.group("link"))
                link = re.sub(r'&amp;', '&', link)

            e = re.sub(r'<!--.*-->', '', str(e))
            e = re.sub(r'</(?:p|span|h6|a|div)>', '\n', e)
            #e = re.sub(r'<img[^>]*>', '\n', e)
            e = re.sub(r'(/액(?!션)|/?(액션|판타지|무협|미분류|단편|완결|단행본|월간|격주))', '', e)
            e = re.sub(r'</?\w+(\s*[\w\-_]+="[^"]*")*/?>', '', e)
            e = re.sub(r'.*\b\d+(화|권|부|편).*', '', e)
            e = re.sub(r'^\s+', '', e)
            e = re.sub(r'\s+$', '\n', e)
            e = re.sub(r'(\s+\n)+', '\n', e)
            if not re.search(r'^\s*$', e):
                title = title + e
            result_list.append((title, link))

    return result_list


def search_site(site_name: str, url_postfix: str, attrs: Dict[str, str], method=Method.GET, headers={}, data={}):
    os.chdir(os.path.join(os.environ["FEED_MAKER_WORK_DIR"], site_name))
    config = json.load(open("site_config.json"))
    content = get_data_from_site(config, url_postfix, method=method, headers=headers, data=data)
    result_list = extract_sub_content_by_attrs(config["url"], content, attrs)
    print_content(site_name, result_list)


def main():
    keyword = urllib.parse.quote(sys.argv[1])
    keyword_cp949 = sys.argv[1].encode("cp949")

    search_site("funbe", "/bbs/search.php?stx=" + keyword, {"class": "section-item-title"})
    search_site("jmana", "/comic_main_frame?keyword=" + keyword, {"path": '//*[@id="wrapCont"]/div/ul/li'})
    search_site("ornson", "/search?skeyword=" + keyword, {"class": "tag_box"})
    search_site("manatoki", "/bbs/search.php?stx=" + keyword, {"class": "media-heading"})
    #search_site("copytoon", "/bbs/search_webtoon.php?stx=" + keyword, {"class": "section-item-title"})
    search_site("wfwf", "/search.html?q=" + urllib.parse.quote(keyword_cp949), {"class": "searchLink"})
    search_site("wtwt", "/sh", {"path": '/html/body/section/div/div[2]/div/div[3]/ul/li'}, method=Method.POST, headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"search_txt": keyword_cp949})

    config = json.load(open(os.path.join(os.environ["FEED_MAKER_WORK_DIR"], "marumaru", "site_config.json")))
    domain = URL.get_url_domain(config["url"])
    search_site("marumaru", "/bbs/search.php?url=https%3A%2F%2F" + domain + "%2Fbbs%2Fsearch.php&stx=" + keyword, {"class": "media-heading"})

    #search_site("manamoa", "/bbs/search.php?url=https%3A%2F%2Fmanamoa34.net%2Fbbs%2Fsearch.php&sfl=0&stx=" + keyword, {"class": "manga-subject"})

    return 0


if __name__ == "__main__":
    sys.exit(main())
