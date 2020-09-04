#!/bin/bash
# macos version
#sudo certbot --authenticator webroot --installer apache --webroot-path $HOME/public_html renew
#echo "httpd를 재실행해야  check_cert.sh를 실행했을 때 인증서의 유효기간이 정상적으로 출력됨"

sudo ~/pkgs/letsencrypt/certbot-auto -d terzeron.com -d www.terzeron.com -d api.terzeron.com -d book.terzeron.com -d fm.terzeron.com -d photo.terzeron.com

