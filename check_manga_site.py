#!/usr/bin/env python


import sys
import os
import re
import json
import logging
import logging.config
from typing import Dict, Any, Optional
from crawler import Crawler, Method
from feed_maker_util import exec_cmd


logging.config.fileConfig(os.environ["FEED_MAKER_HOME_DIR"] + "/bin/logging.conf")
LOGGER = logging.getLogger()


def send_alarm(url: str, new_url: str) -> int:
    cmd = "send_msg_to_line.sh 'no service from %s'" % url
    _, error = exec_cmd(cmd)
    if error:
        print("can't execute a command '%s'" % cmd)
        return -1
    cmd = "send_msg_to_line.sh 'would you check the new site? %s'" % new_url
    _, error = exec_cmd(cmd)
    if error:
        print("can't execute a command '%s'" % cmd)
        return -1
    return 0


def read_config(site_config_file) -> Optional[Dict[str, Any]]:
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
            return config
    return None


def main() -> int:
    do_send: bool = False
    headers: Dict[str, Any] = {}
    site_config_file = "site_config.json"
    if not os.path.isfile(site_config_file):
        print("can't find site config file")
        return -1

    config = read_config(site_config_file)
    if not config:
        return -1

    if not config["render_js"]:
        print("spidering start")
        crawler = Crawler(method=Method.HEAD, headers=headers)
        response = crawler.run(config["url"])
        if response != "200":
            print(response)
            do_send = True
        print("spidering end")

    print("getting start")

    crawler = Crawler(method=Method.GET, num_retries=config["num_retries"], render_js=config["render_js"], encoding=config["encoding"], headers=config["headers"])
    response = None
    try:
        response = crawler.run(config["url"])
        LOGGER.debug(response)
    except BaseException as e:
        LOGGER.error("can't execute crawler")
        LOGGER.debug(e)

    if not response:
        print("no response")
        do_send = True
    else:
        if config["keyword"] not in response:
            print("no keyword")
            do_send = True
        if len(response) <= 10240:
            print("too small response")
            do_send = True

    print("getting end")

    if do_send:
        print("alarming start")
        new_url = re.sub(r'(?P<pre>https?://[\w\.]+\D)(?P<num>\d+)(?P<post>\D.*)', lambda m: m.group("pre") + str(int(m.group("num")) + 1) + m.group("post"), config["url"])
        send_alarm(config["url"], new_url)
        print("alarming end")
        return -1

    print("Ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
