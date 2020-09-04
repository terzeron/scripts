#!/bin/bash
echo | openssl s_client -connect terzeron.net:443 | openssl x509 -noout -dates

