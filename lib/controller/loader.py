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
    conf.MODULE_PLUGIN = dict()
    index = 0
    for _name in conf.MODULE_USE:
        msg = 'Load custom script: %s' % _name
        logger.success(msg)

        if conf.batchfuzz:
            fp, pathname, description = imp.find_module(os.path.splitext(_name)[0], [paths.FUZZ_PATH])
        else:
            fp, pathname, description = imp.find_module(os.path.splitext(_name)[0], [paths.SCRIPT_PATH])
        try:
            index = index + 1
            module_obj = imp.load_module('_' + str(index), fp, pathname, description)
            for each in ESSENTIAL_MODULE_METHODS:
                if not hasattr(module_obj, each):
                    errorMsg = "Can't find essential method:'%s()' in current script，Please modify your script/PoC."
                    sys.exit(logger.error(errorMsg))
            conf.MODULE_PLUGIN[_name] = module_obj
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
        for name,exp in conf.MODULE_PLUGIN.items():
            sub = line.strip()
            if sub:
                module = dict()
                module["sub"] = sub
                module["name"] = name
                module["poc"] = exp
                th.queue.put(module)


def int_mode():
    _int = conf.I_NUM2.strip().split('-')
    for each in range(int(_int[0].strip()), int(_int[1].strip())):
        for name,exp in conf.MODULE_PLUGIN.items():
            module = dict()
            module["sub"] = str(each)
            module["poc"] = exp
            module["name"] = name
            th.queue.put(module)


def net_mode():
    ori_str = conf.NETWORK_STR
    try:
        _list = IPy.IP(ori_str)
    except Exception, e:
        sys.exit(logger.error('Invalid IP/MASK,%s' % e))
    for each in _list:
        for name,exp in conf.MODULE_PLUGIN.items():
            module = dict()
            module["sub"] = str(each)
            module["poc"] = exp
            module["name"] = name
            th.queue.put(module)


def single_target_mode():
    for name,exp in conf.MODULE_PLUGIN.items():
        module = dict()
        module["sub"] = str(conf.SINGLE_TARGET_STR)
        module["poc"] = exp
        module["name"] = name
        th.queue.put(module)


def api_mode():
    conf.API_OUTPUT = os.path.join(paths.DATA_PATH, conf.API_MODE)
    if not os.path.exists(conf.API_OUTPUT):
        os.mkdir(conf.API_OUTPUT)

    file = runApi()
    for line in open(file):
        for name,exp in conf.MODULE_PLUGIN.items():
            module = dict()
            module["sub"] = line.strip()
            module["name"] = name
            if module["sub"]:
                module["poc"] = exp
                th.queue.put(module)
