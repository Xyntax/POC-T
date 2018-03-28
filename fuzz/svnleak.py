#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests
import urlparse

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    url = url + ".svn/all-wcprops"
    try:
        header = dict()
        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        r = requests.get(url, headers=header, timeout=5)
        if "svn:wc:ra_dav:version-url" in r.text:
            return '[Svn Leak]'+url
        else:
            return False
    except Exception:
        return False