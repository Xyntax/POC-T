#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = bit4

import sys
from lib.core.data import paths, logger
from lib.utils.config import ConfigFileParser
from lib.core.common import getSafeExString
import getpass
import urllib
import base64
import json


def check(email, key):
    if email and key:
        auth_url = "https://fofa.so/api/v1/info/my?email={0}&key={1}".format(email, key)
        try:
            response = urllib.urlopen(auth_url)
            if response.code == 200:
                return True
        except Exception, e:
            # logger.error(e)
            return False
    return False


def FofaSearch(query, limit=100, offset=0):  # TODO 付费获取结果的功能实现
    try:
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        logger.info(msg)
        email = ConfigFileParser().FofaEmail()
        key = ConfigFileParser().FofaKey()
        if check(email, key):
            pass
        else:
            raise  # will go to except block
    except:
        msg = 'Automatic authorization failed.'
        logger.warning(msg)
        msg = 'Please input your FoFa Email and API Key below.'
        logger.info(msg)
        email = raw_input("Fofa Email: ").strip()
        key = getpass.getpass(prompt='Fofa API Key: ').strip()
        if not check(email, key):
            msg = 'Fofa API authorization failed, Please re-run it and enter a valid key.'
            sys.exit(logger.error(msg))

    query = base64.b64encode(query)

    request = "https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}".format(email, key, query)
    result = []
    try:
        response = urllib.urlopen(request)
        resp = response.readlines()[0]
        resp = json.loads(resp)
        if not resp["error"]:
            for item in resp.get('results'):
                result.append(item[0])
            if resp.get('size') >= 100:
                logger.info("{0} items found! just 100 returned....".format(resp.get('size')))
    except Exception, e:
        sys.exit(logger.error(getSafeExString(e)))
    finally:
        return result
