#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import os
import glob
import time
import sys
from lib.core.data import conf, paths, th, logger
from lib.core.enums import TARGET_MODE_STATUS, ENGINE_MODE_STATUS
from lib.utils.update import update
from lib.core.enums import API_MODE_NAME
from lib.core.register import Register


def initOptions(args):
    checkUpdate(args)
    checkShow(args)
    EngineRegister(args)
    ScriptRegister(args)
    TargetRegister(args)
    ApiRegister(args)
    Output(args)
    Misc(args)


def checkUpdate(args):
    if args.sys_update:
        update()


def checkShow(args):
    show_scripts = args.show_scripts
    if show_scripts:
        module_name_list = glob.glob(os.path.join(paths.SCRIPT_PATH, '*.py'))
        msg = 'Script Name (total:%s)\n' % str(len(module_name_list) - 1)
        for each in module_name_list:
            _str = os.path.splitext(os.path.split(each)[1])[0]
            if _str not in ['__init__']:
                msg += '  %s\n' % _str
        sys.exit(logger.info(msg))


def EngineRegister(args):
    thread_status = args.engine_thread
    gevent_status = args.engine_gevent
    thread_num = args.thread_num

    def __thread():
        conf.ENGINE = ENGINE_MODE_STATUS.THREAD

    def __gevent():
        conf.ENGINE = ENGINE_MODE_STATUS.GEVENT

    conf.ENGINE = ENGINE_MODE_STATUS.THREAD  # default choice
    conf.batchfuzz = False

    msg = 'Use [-eT] to set Multi-Threaded mode or [-eG] to set Coroutine mode.'
    r = Register(mutex=True, start=0, stop=1, mutex_errmsg=msg)
    r.add(__thread, thread_status)
    r.add(__gevent, gevent_status)
    r.run()

    if 0 < thread_num < 101:
        th.THREADS_NUM = conf.THREADS_NUM = thread_num
    else:
        msg = 'Invalid input in [-t], range: 1 to 100'
        sys.exit(logger.error(msg))

def loadAllPlugins():
    conf.batchfuzz = True
    for dirpath, dirnames, filenames in os.walk(paths.FUZZ_PATH):
        for filename in filenames:
            if '__init__' not in filename and '.pyc' not in filename:
                conf.MODULE_USE.append(filename)

def ScriptRegister(args):
    input_path = args.script_name
    batch = args.batch
    conf.MODULE_USE = []

    # handle input: nothing
    if not (input_path or batch):
        msg = 'Use -s to load script. Example: [-s spider] or [-s ./script/spider.py]'
        sys.exit(logger.error(msg))

    if batch:
        loadAllPlugins()

    # handle input: "-s ./script/spider.py"
    if input_path:
        if os.path.split(input_path)[0]:
            if os.path.exists(input_path):
                if os.path.isfile(input_path):
                    if input_path.endswith('.py'):
                        conf.MODULE_NAME = os.path.split(input_path)[-1]
                        conf.MODULE_FILE_PATH = os.path.abspath(input_path)
                    else:
                        msg = '[%s] not a Python file. Example: [-s spider] or [-s ./script/spider.py]' % input_path
                        sys.exit(logger.error(msg))
                else:
                    msg = '[%s] not a file. Example: [-s spider] or [-s ./script/spider.py]' % input_path
                    sys.exit(logger.error(msg))
            else:
                msg = '[%s] not found. Example: [-s spider] or [-s ./script/spider.py]' % input_path
                sys.exit(logger.error(msg))

        # handle input: "-s spider"  "-s spider.py"
        else:
            if not input_path.endswith('.py'):
                input_path += '.py'
            _path = os.path.abspath(os.path.join(paths.SCRIPT_PATH, input_path))
            if os.path.isfile(_path):
                conf.MODULE_NAME = input_path
                conf.MODULE_FILE_PATH = os.path.abspath(_path)
            else:
                msg = 'Script [%s] not exist. Use [--show] to view all available script in ./script/' % input_path
                sys.exit(logger.error(msg))
        conf.MODULE_USE.append(conf.MODULE_NAME)


def TargetRegister(args):
    input_file = args.target_file
    input_single = args.target_single
    input_network = args.target_network
    input_array = args.target_array
    api_zoomeye = args.zoomeye_dork
    api_shodan = args.shodan_dork
    api_google = args.google_dork
    api_fofa = args.fofa_dork

    def __file():
        if not os.path.isfile(input_file):
            msg = 'TargetFile not found: %s' % input_file
            sys.exit(logger.error(msg))
        conf.TARGET_MODE = TARGET_MODE_STATUS.FILE
        conf.INPUT_FILE_PATH = input_file

    def __array():
        help_str = "Invalid input in [-iA], Example: -iA 1-100"
        try:
            _int = input_array.strip().split('-')
            if int(_int[0]) < int(_int[1]):
                if int(_int[1]) - int(_int[0]) > 1000000:
                    warnMsg = "Loading %d targets, Maybe it's too much, continue? [y/N]" % (
                        int(_int[1]) - int(_int[0]))
                    logger.warning(warnMsg)
                    a = raw_input()
                    if a in ('Y', 'y', 'yes'):
                        pass
                    else:
                        msg = 'User quit!'
                        sys.exit(logger.error(msg))
            else:
                sys.exit(logger.error(help_str))
        except Exception:
            sys.exit(logger.error(help_str))
        conf.TARGET_MODE = TARGET_MODE_STATUS.RANGE
        conf.I_NUM2 = input_array
        conf.INPUT_FILE_PATH = None

    def __network():
        conf.TARGET_MODE = TARGET_MODE_STATUS.IPMASK
        conf.NETWORK_STR = input_network
        conf.INPUT_FILE_PATH = None

    def __single():
        conf.TARGET_MODE = TARGET_MODE_STATUS.SINGLE
        conf.SINGLE_TARGET_STR = input_single
        th.THREADS_NUM = conf.THREADS_NUM = 1
        conf.INPUT_FILE_PATH = None

    def __zoomeye():
        conf.TARGET_MODE = TARGET_MODE_STATUS.API
        conf.API_MODE = API_MODE_NAME.ZOOMEYE
        conf.API_DORK = api_zoomeye

    def __shodan():
        conf.TARGET_MODE = TARGET_MODE_STATUS.API
        conf.API_MODE = API_MODE_NAME.SHODAN
        conf.API_DORK = api_shodan

    def __google():
        conf.TARGET_MODE = TARGET_MODE_STATUS.API
        conf.API_MODE = API_MODE_NAME.GOOGLE
        conf.API_DORK = api_google

    def __fofa():
        conf.TARGET_MODE = TARGET_MODE_STATUS.API
        conf.API_MODE = API_MODE_NAME.FOFA
        conf.API_DORK = api_fofa

    msg = 'Please load targets with [-iS|-iA|-iF|-iN] or use API with [-aZ|-aS|-aG|-aF]'
    r = Register(mutex=True, mutex_errmsg=msg)
    r.add(__file, input_file)
    r.add(__network, input_network)
    r.add(__array, input_array)
    r.add(__single, input_single)
    r.add(__zoomeye, api_zoomeye)
    r.add(__shodan, api_shodan)
    r.add(__google, api_google)
    r.add(__fofa, api_fofa)
    r.run()


def ApiRegister(args):
    search_type = args.search_type
    offset = args.api_offset
    google_proxy = args.google_proxy
    api_limit = args.api_limit

    if not 'API_MODE' in conf:
        return

    if not conf.API_DORK:
        msg = 'Empty API dork, show usage with [-h]'
        sys.exit(logger.error(msg))

    if offset < 0:
        msg = 'Invalid value in [--offset], show usage with [-h]'
        sys.exit(logger.error(msg))
    else:
        conf.API_OFFSET = offset

    # handle typeError in cmdline.py
    if api_limit <= 0:
        msg = 'Invalid value in [--limit], show usage with [-h]'
        sys.exit(logger.error(msg))
    else:
        conf.API_LIMIT = api_limit

    if conf.API_MODE is API_MODE_NAME.ZOOMEYE:
        if search_type not in ['web', 'host']:
            msg = 'Invalid value in [--search-type], show usage with [-h]'
            sys.exit(logger.error(msg))
        else:
            conf.ZOOMEYE_SEARCH_TYPE = search_type

    elif conf.API_MODE is API_MODE_NAME.GOOGLE:
        conf.GOOGLE_PROXY = google_proxy


def Output(args):
    output_file = args.output_path
    file_status = args.output_file_status
    screen_status = args.output_screen_status
    browser = args.open_browser

    if not file_status and output_file:
        msg = 'Cannot use [-oF] and [-o] together, please read the usage with [-h].'
        sys.exit(logger.error(msg))

    if not file_status and browser:
        msg = '[--browser] is based on file output, please remove [-oF] in your command and try again.'
        sys.exit(logger.error(msg))

    conf.SCREEN_OUTPUT = screen_status
    conf.FILE_OUTPUT = file_status
    conf.OUTPUT_FILE_PATH = os.path.abspath(output_file) if output_file else \
        os.path.abspath(
            os.path.join(
                paths.OUTPUT_PATH, time.strftime(
                    '[%Y%m%d-%H%M%S]', time.localtime(
                        time.time())) + '.txt'))


def Misc(args):
    conf.SINGLE_MODE = args.single_mode
    conf.OPEN_BROWSER = args.open_browser
