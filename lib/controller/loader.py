#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import Queue
import sys
import imp
import os
from lib.core.data import th, conf, logger, paths
from lib.core.enums import API_MODE_NAME, TARGET_MODE_STATUS
from lib.core.settings import ESSENTIAL_MODULE_METHODS
from lib.core.exception import ToolkitValueException
from lib.controller.api import runApi
from thirdparty.IPy import IPy


def loadModule():
    _name = conf.MODULE_NAME
    msg = 'Load custom script: %s' % _name
    logger.success(msg)

    fp, pathname, description = imp.find_module(os.path.splitext(_name)[0], [paths.SCRIPT_PATH])
    try:
        th.module_obj = imp.load_module("_", fp, pathname, description)
        for each in ESSENTIAL_MODULE_METHODS:
            if not hasattr(th.module_obj, each):
                errorMsg = "Can't find essential method:'%s()' in current script，Please modify your script/PoC." % each
                sys.exit(logger.error(errorMsg))
    except ImportError, e:
        errorMsg = "Your current scipt [%s.py] caused this exception\n%s\n%s" \
                   % (_name, '[Error Msg]: ' + str(e), 'Maybe you can download this module from pip or easy_install')
        sys.exit(logger.error(errorMsg))


def loadPayloads():
    infoMsg = 'Initialize targets...'
    logger.success(infoMsg)
    th.queue = Queue.Queue()
    if conf.TARGET_MODE is TARGET_MODE_STATUS.RANGE:
        int_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.FILE:
        file_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.IPMASK:
        net_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.SINGLE:
        single_target_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.API:
        api_mode()

    else:
        raise ToolkitValueException('conf.TARGET_MODE value ERROR.')
    logger.success('Total: %s' % str(th.queue.qsize()))


def file_mode():
    for line in open(conf.INPUT_FILE_PATH):
        sub = line.strip()
        if sub:
            th.queue.put(sub)


def int_mode():
    _int = conf.I_NUM2.strip().split('-')
    for each in range(int(_int[0].strip()), int(_int[1].strip())):
        th.queue.put(str(each))


def net_mode():
    ori_str = conf.NETWORK_STR
    try:
        _list = IPy.IP(ori_str)
    except Exception, e:
        sys.exit(logger.error('Invalid IP/MASK,%s' % e))
    for each in _list:
        th.queue.put(str(each))


def single_target_mode():
    th.queue.put(str(conf.SINGLE_TARGET_STR))


def api_mode():
    conf.API_OUTPUT = os.path.join(paths.DATA_PATH, conf.API_MODE)
    if not os.path.exists(conf.API_OUTPUT):
        os.mkdir(conf.API_OUTPUT)

    file = runApi()
    for line in open(file):
        sub = line.strip()
        if sub:
            th.queue.put(sub)
