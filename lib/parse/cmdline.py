#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import argparse
import sys
from lib.core.settings import VERSION


def cmdLineParser():
    parser = argparse.ArgumentParser(description='powered by cdxy <mail:i@cdxy.me> ',
                                     usage='python POC-T.py -s bingc -aZ "port:8080"',
                                     add_help=False)

    engine = parser.add_argument_group('ENGINE')
    engine.add_argument('-eT', dest="engine_thread", default=False, action='store_true',
                        help='Multi-Threaded engine (default choice)')

    engine.add_argument('-eG', dest="engine_gevent", default=False, action='store_true',
                        help='Gevent engine (single-threaded with asynchronous)')

    engine.add_argument('-t', metavar='NUM', dest="thread_num", type=int, default=10,
                        help='num of threads/concurrent, 10 by default')

    script = parser.add_argument_group('SCRIPT')

    script.add_argument('-s', metavar='NAME', dest="script_name", type=str, default='',
                        help='load script by name (-s jboss-rce) or path (-s ./script/jboss.py)')
    script.add_argument('--batch',dest="batch",default=False,action='store_true',
                        help='batch fuzz using fuzz script')

    target = parser.add_argument_group('TARGET')

    target.add_argument('-iS', metavar='TARGET', dest="target_single", type=str, default='',
                        help="scan a single target (e.g. www.wooyun.org)")
    target.add_argument('-iF', metavar='FILE', dest="target_file", type=str, default='',
                        help='load targets from targetFile (e.g. ./data/wooyun_domain)')
    target.add_argument('-iA', metavar='START-END', dest="target_array", type=str, default='',
                        help='generate array from int(start) to int(end) (e.g. 1-100)')
    target.add_argument('-iN', metavar='IP/MASK', dest="target_network", type=str, default='',
                        help='generate IP from IP/MASK. (e.g. 127.0.0.0/24)')

    api = parser.add_argument_group('API')
    api.add_argument('-aZ', '--zoomeye', metavar='DORK', dest="zoomeye_dork", type=str, default='',
                     help='ZoomEye dork (e.g. "zabbix port:8080")')
    api.add_argument('-aS', '--shodan', metavar='DORK', dest="shodan_dork", type=str, default='',
                     help='Shodan dork.')
    api.add_argument('-aG', '--google', metavar='DORK', dest="google_dork", type=str, default='',
                     help='Google dork (e.g. "inurl:admin.php")')
    api.add_argument('-aF', '--fofa', metavar='DORK', dest="fofa_dork", type=str, default='',
                     help='FoFa dork (e.g. "banner=users && protocol=ftp")')
    api.add_argument('--limit', metavar='NUM', dest="api_limit", type=int, default=10,
                     help='Maximum searching results (default:10)')
    api.add_argument('--offset', metavar='OFFSET', dest="api_offset", type=int, default=0,
                     help="Search offset to begin getting results from (default:0)")
    api.add_argument('--search-type', metavar='TYPE', dest="search_type", action="store", default='host',
                     help="[ZoomEye] search type used in ZoomEye API, web or host (default:host)")
    api.add_argument('--gproxy', metavar='PROXY', dest="google_proxy", action="store", default=None,
                     help="[Google] Use proxy for Google (e.g. \"sock5 127.0.0.1 7070\" or \"http 127.0.0.1 1894\"")

    output = parser.add_argument_group('OUTPUT')

    output.add_argument('-o', metavar='FILE', dest="output_path", type=str, default='',
                        help='output file path&name. default in ./output/')
    output.add_argument('-oF', '--no-file', dest="output_file_status", default=True, action='store_false',
                        help='disable file output')
    output.add_argument('-oS', '--no-screen', dest="output_screen_status", default=True, action='store_false',
                        help='disable screen output')

    misc = parser.add_argument_group('MISC')

    misc.add_argument('--single', dest="single_mode", default=False, action='store_true',
                      help='exit after finding the first victim/password.')
    misc.add_argument('--show', dest="show_scripts", default=False, action='store_true',
                      help='show available script names in ./script/ and exit')
    misc.add_argument('--browser', dest="open_browser", default=False, action='store_true',
                      help='Open notepad or web browser to view report after task finished.')

    system = parser.add_argument_group('SYSTEM')

    system.add_argument('-v', '--version', action='version', version=VERSION,
                        help="show program's version number and exit")
    system.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')
    system.add_argument('--update', dest="sys_update", default=False, action='store_true',
                        help='update POC-T from github source')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args
