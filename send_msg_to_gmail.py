#!/usr/bin/env python


import re
import sys
import getopt
import json
from pathlib import Path
from shutil import which
import requests


class Mailer():
    def __init__(self):
        self.mail_sender = "terzeron@terzeron.com"
        self.mail_sender_name = "조영일"

        program_full_path = which(sys.argv[0])
        if program_full_path:
            conf_file_path = Path(program_full_path).parent / "global_config.json"
            with conf_file_path.open("r", encoding="utf-8") as infile:
                content = infile.read()
                data = json.loads(content)
                if "nhn_cloud_appkey" in data and data["nhn_cloud_appkey"]:
                    self.appkey = data["nhn_cloud_appkey"]
                if "nhn_cloud_secretkey" in data and data["nhn_cloud_secretkey"]:
                    self.secretkey = data["nhn_cloud_secretkey"]
                if "mail_sender_address" in data and data["mail_sender_address"]:
                    self.sender = data["mail_sender_address"]
                if "mail_recipient_address" in data and data["mail_recipient_address"]:
                    self.recipients = [ data["mail_recipient_address"] ]
                    
    def send_mail(self, subject, body) -> bool:
        url = f"https://email.api.nhncloudservice.com/email/v2.0/appKeys/{self.appkey}/sender/mail"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-Secret-Key": self.secretkey
        }
        receiver_list = []
        for recipient in self.recipients:
            name, address = re.split(r'[, ]+', recipient)
            receiver_list.append({
                "receiveMailAddr": address,
                "receiveName": name,
                "receiveType": "MRT0"
            })
        payload = {
            "senderAddress": self.mail_sender,
            "senderName": self.mail_sender_name,
            "title": subject,
            "body": body,
            "receiverList": receiver_list
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        if response and response.status_code == 200:
            r = json.loads(response.text)
            if r["header"]["isSuccessful"]:
                print("Success in sending a mail")
                return True

        print("Error in sending a mail")
        print(response.text)
        return False


def print_usage(program: str):
    print(f"Usage: {program} [-s \"subject\"]")
    print()
    print(f"echo \"message\" | {program}")
    print(f"echo \"message\" | {program} -s \"subject\"")
    print(f"{program} -s \"subject\" \"message\"")
    print(f"{program} \"message\"")
    print()
    sys.exit(0)


def main() -> int:
    subject = "Notification from terzeron.com"
    body = ""

    optlist, args = getopt.getopt(sys.argv[1:], "s:h")
    for o, a in optlist:
        if o == "-s":
            subject = a
        if o == "-h":
            print_usage(sys.argv[0])

    if len(args) > 0:
        body = args[0]
    else:
        body = sys.stdin.read().rstrip()
        lines = body.split("\n")
        body = "<br>\n".join(lines)

    mailer = Mailer()
    #print(f"subject='{subject}', body='{body}'")
    if not mailer.send_mail(subject, body):
        return -1

    return 0


if __name__ == "__main__":
    sys.exit(main())
