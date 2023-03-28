#!/usr/bin/env python


import sys
import base64
import hmac
import hashlib
import getopt
import datetime
import json
from pathlib import Path
from typing import Tuple
from shutil import which
import requests


class Mailer():
    def __init__(self):
        program_full_path = which(sys.argv[0])
        if program_full_path:
            conf_file_path = Path(program_full_path).parent / "global_config.json"
            with conf_file_path.open("r", encoding="utf-8") as infile:
                content = infile.read()
                data = json.loads(content)
                if "naver_cloud_access_key" in data and data["naver_cloud_access_key"]:
                    self.access_key = data["naver_cloud_access_key"]
                if "naver_cloud_secret_key" in data and data["naver_cloud_secret_key"]:
                    self.secret_key = data["naver_cloud_secret_key"]
                if "nhn_cloud_appkey" in data and data["nhn_cloud_appkey"]:
                    self.appkey = data["nhn_cloud_appkey"]
                if "nhn_cloud_secretkey" in data and data["nhn_cloud_secretkey"]:
                    self.secretkey = data["nhn_cloud_secretkey"]
                if "mail_sender_address" in data and data["mail_sender_address"]:
                    self.sender = data["mail_sender_address"]
                if "mail_recipient_address" in data and data["mail_recipient_address"]:
                    self.recipient = data["mail_recipient_address"]
                    

    def __del__(self):
        del self.access_key
        del self.secret_key
        del self.sender
        del self.recipient
                                         

    def make_signature(self) -> Tuple[str, int]:
        space = " "  # 공백
        new_line = "\n"  # 줄바꿈
        method = "POST"  # HTTP 메소드
        url = "/api/v1/mails"  # 도메인을 제외한 "/" 아래 전체 url (쿼리스트링 포함)
        timestamp = int(datetime.datetime.now().timestamp()) * 1000
        message = f"{method}{space}{url}{new_line}{timestamp}{new_line}{self.access_key}"
        signing_key = hmac.new(self.secret_key.encode('UTF-8'), message.encode('UTF-8'), hashlib.sha256)
        raw_hmac = signing_key.digest()
        encode_base64_string = base64.b64encode(raw_hmac).decode('UTF-8')
        return encode_base64_string, timestamp

    def send_mail(self, subject, body) -> None:
        signature, timestamp = self.make_signature()
        url = "https://mail.apigw.ntruss.com/api/v1/mails"
        headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": str(timestamp),
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature
        }
        payload = {
            "senderAddress": self.sender,
            "recipients": [
                {
                    "address": self.recipient,
                    "name": "조영일",
                    "type": "R"
                }
            ],
            "individual": True,
            "advertising": False,
            "title": subject,
            "body": body
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        if response:
            result = json.loads(response.content)
            if "count" in result and result["count"] > 0:
                print("Success in sending a mail")
        else:
            print("Error in sending a mail")


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
    mailer.send_mail(subject, body)

    return 0


if __name__ == "__main__":
    sys.exit(main())
