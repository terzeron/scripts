#!/bin/bash

sudo certbot renew -d terzeron.com -d www.terzeron.com -d api.terzeron.com -d book.terzeron.com -d fm.terzeron.com -d photo.terzeron.com -d wiki.terzeron.com -d grafana.terzeron.com --apache

