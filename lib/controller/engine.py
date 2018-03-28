#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import threading
import time
import traceback
from lib.core.data import th, conf, logger
from lib.core.common import dataToStdout
from lib.utils.console import getTerminalSize
from lib.utils.versioncheck import PYVERSION
from lib.core.enums import POC_RESULT_STATUS, ENGINE_MODE_STATUS


def initEngine():
    th.thread_mode = True if conf.ENGINE is ENGINE_MODE_STATUS.THREAD else False
    th.f_flag = conf.FILE_OUTPUT
    th.s_flag = conf.SCREEN_OUTPUT
    th.output = conf.OUTPUT_FILE_PATH
    th.thread_count = th.threads_num = th.THREADS_NUM
    th.single_mode = conf.SINGLE_MODE
    th.scan_count = th.found_count = 0
    th.console_width = getTerminalSize()[0] - 2
    th.is_continue = True
    th.found_single = False
    th.start_time = time.time()
    setThreadLock()
    msg = 'Set the number of concurrent: %d' % th.threads_num
    logger.success(msg)


def singleMode():
    th.is_continue = False
    th.found_single = True


def scan():
    while 1:
        if th.thread_mode: th.load_lock.acquire()
        if th.queue.qsize() > 0 and th.is_continue:
            module = th.queue.get(timeout=1.0)
            payload = str(module["sub"])
            module_obj = module["poc"]
            if th.thread_mode: th.load_lock.release()
        else:
            if th.thread_mode: th.load_lock.release()
            break
        try:
            # POC在执行时报错如果不被处理，线程框架会停止并退出
            status = module_obj.poc(payload)
            resultHandler(status, module)
        except Exception:
            th.errmsg = traceback.format_exc()
            th.is_continue = False
        changeScanCount(1)
        if th.s_flag:
            printProgress()
    if th.s_flag:
        printProgress()

    changeThreadCount(-1)


def run():
    initEngine()
    if conf.ENGINE is ENGINE_MODE_STATUS.THREAD:
        for i in range(th.threads_num):
            t = threading.Thread(target=scan, name=str(i))
            setThreadDaemon(t)
            t.start()
        # It can quit with Ctrl-C
        while 1:
            if th.thread_count > 0 and th.is_continue:
                time.sleep(0.01)
            else:
                break

    elif conf.ENGINE is ENGINE_MODE_STATUS.GEVENT:
        from gevent import monkey
        monkey.patch_all()
        import gevent
        while th.queue.qsize() > 0 and th.is_continue:
            gevent.joinall([gevent.spawn(scan) for i in xrange(0, th.threads_num) if
                            th.queue.qsize() > 0])

    dataToStdout('\n')

    if 'errmsg' in th:
        logger.error(th.errmsg)

    if th.found_single:
        msg = "[single-mode] found!"
        logger.info(msg)


def resultHandler(status, payload):
    def printScrren(msg):    
        if th.s_flag:
            printMessage(msg)
        if th.f_flag:
            output2file(msg)
        if th.single_mode:
            singleMode()
    if not status or status is POC_RESULT_STATUS.FAIL:
        return
    elif status is POC_RESULT_STATUS.RETRAY:
        changeScanCount(-1)
        th.queue.put(payload)
        return
    elif status is True or status is POC_RESULT_STATUS.SUCCESS:
        msg = payload["sub"] + " -" + payload["name"]
        printScrren(msg)
    else:
        if type(status) == set:
            for x in status:
                printScrren(str(x))
        elif type(status) == list:
            for x in status:
                printScrren(str(x))
        else:
            msg = str(status)
            printScrren(msg)
    changeFoundCount(1)

    


def setThreadLock():
    if th.thread_mode:
        th.found_count_lock = threading.Lock()
        th.scan_count_lock = threading.Lock()
        th.thread_count_lock = threading.Lock()
        th.file_lock = threading.Lock()
        th.load_lock = threading.Lock()


def setThreadDaemon(thread):
    # Reference: http://stackoverflow.com/questions/190010/daemon-threads-explanation
    if PYVERSION >= "2.6":
        thread.daemon = True
    else:
        thread.setDaemon(True)


def changeFoundCount(num):
    if th.thread_mode: th.found_count_lock.acquire()
    th.found_count += num
    if th.thread_mode: th.found_count_lock.release()


def changeScanCount(num):
    if th.thread_mode: th.scan_count_lock.acquire()
    th.scan_count += num
    if th.thread_mode: th.scan_count_lock.release()


def changeThreadCount(num):
    if th.thread_mode: th.thread_count_lock.acquire()
    th.thread_count += num
    if th.thread_mode: th.thread_count_lock.release()


def printMessage(msg):
    dataToStdout('\r' + msg + ' ' * (th.console_width - len(msg)) + '\n\r')


def printProgress():
    msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
        th.found_count, th.queue.qsize(), th.scan_count, time.time() - th.start_time)
    out = '\r' + ' ' * (th.console_width - len(msg)) + msg
    dataToStdout(out)


def output2file(msg):
    if th.thread_mode: th.file_lock.acquire()
    f = open(th.output, 'a')
    f.write(msg + '\n')
    f.close()
    if th.thread_mode: th.file_lock.release()
