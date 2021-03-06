#!/usr/bin/env python


import sys
import os
import re
import json
import logging
import logging.config
from feed_maker_util import exec_cmd


logging.config.fileConfig(os.environ["FEED_MAKER_HOME_DIR"] + "/bin/logging.conf")
LOGGER = logging.getLogger()


def print_usage() -> None:
    print("Usage:\t%s <site number>")


def update_domain() -> bool:
    print("--- updating domain ---")
    new_postfix = sys.argv[1]

    # update site config file
    print("- site_config.json")
    site_config_file = "site_config.json"
    if not os.path.isfile(site_config_file):
        print("can't find site config file")
        return False

    with open(site_config_file, "r") as f:
        site_config = json.load(f)
        if site_config:
            if "url" in site_config:
                new_url = re.sub(r'(?P<pre>https?://[\w\.\-]+\D)(?P<variant_postfix>\d+|\.\w+)(?P<post>[^/]*)', r'\g<pre>' + new_postfix + r'\g<post>', site_config["url"])
            else:
                print("no url in site config")
                return False

    with open(site_config_file, "w") as f:
        site_config["url"] = new_url
        json.dump(site_config, f, ensure_ascii=False)

    print("- git add")
    git_cmd: str = "git add %s" % site_config_file
    _, error = exec_cmd(git_cmd)
    if error:
        LOGGER.error("can't execute a command '%s', %s", git_cmd, error)

    # update config files of all feeds which belongs to the site
    for entry in os.listdir("."):
        if not os.path.isdir(os.path.join(".", entry)) or entry.startswith("."):
            continue
        print("- %s: " % entry, end='')
        conf_file = os.path.join(entry, "conf.xml")
        print(".", end='')
        ifile = open(conf_file, "r")
        temp_conf_file = conf_file + ".temp"
        ofile = open(temp_conf_file, "w")
        for line in ifile:
            m = re.search(r'(?P<pre><list_url><!\[CDATA\[https?://[\w\.\-]+\D)(?P<variant_postfix>\d+|\.\w+)(?P<post>(\.|/).*]]></list_url>)', line)
            if m:
                line = "            " + m.group("pre") + new_postfix + m.group("post") + "\n"
            ofile.write(line)
        ifile.close()
        ofile.close()
        os.rename(temp_conf_file, conf_file)

        print(".", end='')
        git_cmd: str = "git add %s" % conf_file
        _, error = exec_cmd(git_cmd)
        if error:
            LOGGER.error("can't execute a command '%s', %s", git_cmd, error)

        print(".", end='')
        if os.path.isdir(os.path.join(".", entry, "newlist")):
            for e in os.listdir(os.path.join(".", entry, "newlist")):
                os.remove(os.path.join(".", entry, "newlist", e))
            os.rmdir(os.path.join(".", entry, "newlist"))

        print(".", end='')
        try:
            os.remove(os.path.join(".", entry, entry + ".xml"))
            os.remove(os.path.join(".", entry, entry + ".xml.old"))
        except FileNotFoundError:
            pass
        print("")

    print("- git commit")
    git_cmd: str = "git commit -m 'modify site url'"
    _, error = exec_cmd(git_cmd)
    if error:
        LOGGER.error("can't execute a command '%s', %s", git_cmd, error)

    return True


def check_site() -> bool:
    print("--- checking site ---")
    cmd = "check_manga_site.py"
    result, error = exec_cmd(cmd)
    if result:
        print(result)
    else:
        print(error)
    return True


def main():
    if len(sys.argv) < 2:
        print_usage()
        return -1

    if update_domain():
        check_site()

    return 0

        
if __name__ == "__main__":
    sys.exit(main())
