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
    LOGGER.debug("# get_data_from_site(config=%r, url_postfix=%s, method=%s, headers=%r, data=%r)", config, url_postfix, method, headers, data)
    url_prefix: str = URL.get_url_scheme(config["url"]) + "://" + URL.get_url_domain(config["url"])
    encoding: str = config["encoding"] if "encoding" in config else None
    render_js: bool = config["render_js"] if "render_js" in config else False
    c: Crawler = Crawler(render_js=render_js, method=method, headers=headers, encoding=encoding)
    url: str = url_prefix + url_postfix
    response, _ = c.run(url=url, data=data)
    return response


def extract_sub_content_by_attrs(search_url: str, content: str, attrs: Dict[str, str]) -> List[Tuple[str, str]]:
    LOGGER.debug("# extract_sub_content_by_attrs(search_url=%s, content=%s, attrs=%r)", search_url, content, attrs)
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
                    # jmana의 경우 버그
                    link = URL.concatenate_url(search_url, m.group("link"))
                link = re.sub(r'&amp;', '&', link)

            e = re.sub(r'<!--.*-->', '', str(e))
            e = re.sub(r'</(?:p|span|h6|a|div)>', '\n', e)
            #e = re.sub(r'<img[^>]*>', '\n', e)
            e = re.sub(r'(만화제목|작가이름|발행검색|초성검색|장르검색|정렬|검색 결과|나의 댓글 반응|공지사항|북마크업데이트|북마크|주간랭킹 TOP30|나의 글 반응|오늘|한달 전|주간|격주|월간|단행본|단편|완결)', '', e)
            e = re.sub(r'(/액(?!션)|/?(액션|판타지|무협|미분류|단편|완결|단행본|월간|격주|연재))', '', e)
            e = re.sub(r'</?\w+(\s*[\w\-_]+="[^"]*")*/?>', '', e)
            e = re.sub(r'.*\b\d+(화|권|부|편).*', '', e)
            e = re.sub(r'\#\[\]', '', e)
            e = re.sub(r'^(\s|\n)+', '', e)
            e = re.sub(r'\s+$', '\n', e)
            e = re.sub(r'(\s+\n)+', '\n', e)
            if not re.search(r'^\s*$', e):
                title = e
            if title and link:
                result_list.append((title, link))

    return result_list


def search_site(site_name: str, url_postfix: str, attrs: Dict[str, str], method=Method.GET, headers={}, data={}):
    LOGGER.debug("# search_site(site_name=%s, url_postfix=%s, attrs=%r, method=%s, headers=%r, data=%r)", site_name, url_postfix, attrs, method, headers, data)
    os.chdir(os.path.join(os.environ["FEED_MAKER_WORK_DIR"], site_name))
    config = json.load(open("site_config.json"))
    content = get_data_from_site(config, url_postfix, method=method, headers=headers, data=data)
    result_list = extract_sub_content_by_attrs(config["url"], content, attrs)
    print_content(site_name, result_list)


def main():
    LOGGER.debug("# main()")
    keyword = urllib.parse.quote(sys.argv[1])
    keyword_cp949 = sys.argv[1].encode("cp949")

    #search_site("funbe", "/bbs/search.php?stx=" + keyword, {"class": "section-item-title"})
    search_site("jmana", "/comic_list?keyword=" + keyword, {"class": "tit"})
    search_site("ornson", "/search?skeyword=" + keyword, {"class": "tag_box"})
    search_site("manatoki", "/comic?stx=" + keyword, {"class": "list-item"})
    search_site("copytoon", "/bbs/search_webtoon.php?stx=" + keyword, {"class": "section-item-title"})
    search_site("wfwf", "/search.html?q=" + urllib.parse.quote(keyword_cp949), {"class": "searchLink"})
    search_site("wtwt", "/sh", {"path": '/html/body/section/div/div[2]/div/div[3]/ul/li'}, method=Method.POST, headers={"Content-Type": "application/x-www-form-urlencoded"}, data={"search_txt": keyword_cp949})

    config = json.load(open(os.path.join(os.environ["FEED_MAKER_WORK_DIR"], "marumaru", "site_config.json")))
    domain = URL.get_url_domain(config["url"])
    search_site("marumaru", "/bbs/search.php?url=https%3A%2F%2F" + domain + "%2Fbbs%2Fsearch.php&stx=" + keyword, {"class": "media-heading"})

    #search_site("manamoa", "/bbs/search.php?url=https%3A%2F%2Fmanamoa34.net%2Fbbs%2Fsearch.php&sfl=0&stx=" + keyword, {"class": "manga-subject"})

    return 0


if __name__ == "__main__":
    sys.exit(main())
