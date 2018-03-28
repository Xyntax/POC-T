#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests
import re
from bs4 import BeautifulSoup
import urlparse

class spiderMain(object):

    def __init__(self,url):
        self.SIMILAR_SET = set()
        self.link = url

    def judge(self,url):
        # 先将URL链接，然后判断是否在origin
        # 在判断?/aspx/asp/php/jsp 是否在里面
        origin = self.link
        new_url = urlparse.urljoin(origin,url)
        domain = urlparse.urlparse(origin).netloc
        
        if domain not in new_url:
            return False
        if self.url_similar_check(new_url) == False:
            return False
        if '=' in new_url and ('aspx' in new_url or 'asp' in new_url or 'php' in new_url or 'jsp' in new_url):
            return new_url
        else:
            return False

    def url_similar_check(self,url):
        '''
        URL相似度分析
        当url路径和参数键值类似时，则判为重复
        '''
        url_struct = urlparse.urlparse(url)
        query_key = '|'.join(sorted([i.split('=')[0] for i in url_struct.query.split('&')]))
        url_hash = hash(url_struct.path + query_key)
        if url_hash not in self.SIMILAR_SET:
            self.SIMILAR_SET.add(url_hash)
            return True
        return False

    def run(self):
        header = dict()
        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        header["Referer"] = "http://www.qq.com"
        new_urls = set()
        try:
            r = requests.get(self.link, headers=header, timeout=5)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                
                links = soup.find_all('a')
                for link in links:
                    new_url = link.get('href')
                    full_url = self.judge(new_url)
                    if full_url:
                        new_urls.add(full_url)
            else:
                return False
        except Exception:
            return False
        finally:
            if new_urls:
                return new_urls
            else:
                return False

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    s = spiderMain(url)
    f = s.run()
    return f
