#!/usr/bin/env python


import sys
import os
import re
import json
import logging
import logging.config
from typing import Dict, Any, Optional, Tuple
from crawler import Crawler, Method
from feed_maker_util import exec_cmd, URL


logging.config.fileConfig(os.environ["FEED_MAKER_HOME_DIR"] + "/bin/logging.conf")
LOGGER = logging.getLogger()


def send_alarm(url: str, new_url: str) -> int:
    LOGGER.debug("# send_alarm(url=%s, new_url=%s)", url, new_url)
    print("alarming start")
    ret = 0
    msg = "no service from %s\nwould you check the new site? %s" % (url, new_url)
    cmd = "send_msg_to_gmail.sh '%s'" % msg
    _, error = exec_cmd(cmd)
    if error:
        print("can't execute a command '%s'" % cmd)
        ret = -1
    print("alarming end")
    return ret


def read_config(site_config_file) -> Optional[Dict[str, Any]]:
    LOGGER.debug("# read_config(site_config_file=%r)", site_config_file)
    with open(site_config_file, "r") as f:
        config = json.load(f)
        if config:
            if "url" not in config:
                print("no url in site config")
                return None
            if "keyword" not in config:
                print("no keyword in site config")
                return None
            if "num_retries" not in config:
                config["num_retries"] = 1
            if "encoding" not in config:
                config["encoding"] = "utf-8"
            if "headers" not in config:
                config["headers"] = {}
            if "timeout" not in config:
                config["timeout"] = 10
            return config
    return None


def get_location(headers: Dict[str, Any]):
    LOGGER.debug("# get_location(headers=%r)", headers)
    new_url = ""
    if headers and "Location" in headers:
        new_url = headers["Location"]
    return new_url


def spider(url: str, config: Dict[str, Any]) -> str:
    LOGGER.debug("# spider(url=%s, config=%r)", url, config)
    do_send = False
    new_url = ""
    print("spidering start")
    crawler = Crawler(method=Method.HEAD, headers=config["headers"])
    response, response_headers = crawler.run(url)
    #LOGGER.debug("response=%s, response_headers=%r", response, response_headers)
    if response != "200":
        if response_headers:
            new_url = get_location(response_headers)
            if new_url.startswith("//"):
                new_url = URL.get_url_scheme(url) + ":" + new_url
        do_send = True
    print("spidering end")
    return do_send, new_url


def get(url: str, config: Dict[str, Any]) -> Tuple[bool, str, str]:
    LOGGER.debug("# get(url=%s, config=%r)", url, config)
    print("getting start")
    new_url = ""
    do_send = False
    response = None
    response_headers = None
    crawler = Crawler(method=Method.GET, num_retries=config["num_retries"], render_js=config["render_js"], encoding=config["encoding"], headers=config["headers"], timeout=config["timeout"])
    response, response_headers = crawler.run(url)
    #LOGGER.debug("response=%s, response_headers=%r", response, response_headers)
    if response_headers:
        new_url = get_location(response_headers)
        if new_url:
            print("new_url=%s" % new_url)
    
    if not response:
        print("no response")
        do_send = True
    else:
        if config["keyword"] not in response:
            print("no keyword")
            do_send = True
        if URL.get_url_domain(url) not in response:
            print("old url not found")
            do_send = True
    print("getting end")
    return do_send, response, new_url
    

def get_new_url(url: str, response: str, new_pattern: str, pre: str, domain_postfix: str, post: str) -> str:
    LOGGER.debug("# get_new_url(url=%s, response, new_pattern=%s, pre=%s, domain_postfix=%s, post=%s)", url, new_pattern, pre, domain_postfix, post)
    new_url: str = ""
    # try to find similar url
    url_count_map: Dict[str, int] = {}
    matches = re.findall(new_pattern, str(response))
    for match in matches:
        new_url = pre + match + domain_postfix + post
        LOGGER.debug("new_url=%s", new_url)
        if new_url in url_count_map:
            url_count_map[new_url] += 1
        else:
            url_count_map[new_url] = 1

    if len(url_count_map) == 0:
        print("can't find new url")
        new_url = ""
    else:
        dict(sorted(url_count_map.items(), key=lambda item: item[1], reverse=True))
        new_url = list(url_count_map.keys())[0]
    return new_url


def get_url_pattern(url: str) -> Tuple[str, str, str]:
    LOGGER.debug("# get_url_pattern(url=%s)", url)
    new_pattern: str = ""
    pre: str = ""
    domain_postfix: str = ""
    post: str = ""
    m1 = re.search(r'(?P<pre>https?://[\w\.\-]+\D)(?P<num>\d+)(?P<domain_postfix>[^/]+)(?P<post>.*)', url)
    m2 = re.search(r'(?P<pre>https?://[\w\.\-]+)\.[^/]+(?P<post>.*)', url)
    if m1 or m2:
        if m1:
            pre = m1.group("pre")
            domain_postfix = m1.group("domain_postfix")
            post = m1.group("post")
            new_pattern = pre + '(\d+)' + domain_postfix + '(?:' + post + ')?'
            LOGGER.debug("first pattern: %s, %s, %s, %s", pre, domain_postfix, post, new_pattern)
        elif m2:
            pre = m2.group("pre")
            post = m2.group("post")
            new_pattern = pre + '(\.[^/]+)' + post
            LOGGER.debug("second pattern: %s, %s, %s", pre, post, new_pattern)
    return new_pattern, pre, domain_postfix, post

            
def main() -> int:
    LOGGER.debug("# main()")
    do_send: bool = False
    new_url = ""
    site_config_file = "site_config.json"
    if not os.path.isfile(site_config_file):
        print("can't find site config file")
        return -1

    config = read_config(site_config_file)
    if not config:
        print("can't read configuration file '%s'" % site_config_file)
        return -1
    url = config["url"]
    print("url=%s" % url)

    try:
        os.remove("cookies.json")
    except FileNotFoundError:
        pass

    new_pattern, pre, domain_postfix, post = get_url_pattern(url)
    
    if not config["render_js"]:
        do_send, new_url = spider(url, config)
        if do_send:
            print("can't get access to url '%s'" % url)
            send_alarm(url, new_url)
            return 0
        
    do_send, response, new_url = get(url, config)
    if do_send:
        if not new_url:
            new_url = get_new_url(url, response, new_pattern, pre, domain_postfix, post)
        if url != new_url:
            print("New url: '%s'" % new_url)
            send_alarm(url, new_url)
            return 0

    print("Ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
