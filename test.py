#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

from difflib import SequenceMatcher
import requests
import re

def getFilteredPageContent(page, onlyText=True, split=" "):
    """
    Returns filtered page content without script, style and/or comments
    or all HTML tags

    >>> getFilteredPageContent(u'<html><title>foobar</title><body>test</body></html>')
    u'foobar test'
    """

    retVal = page

    # only if the page's charset has been successfully identified
    if isinstance(page, unicode):
        retVal = re.sub(r"(?si)<script.+?</script>|<!--.+?-->|<style.+?</style>%s" % (r"|<[^>]+>|\t|\n|\r" if onlyText else ""), split, page)
        while retVal.find(2 * split) != -1:
            retVal = retVal.replace(2 * split, split)
        retVal = htmlunescape(retVal.strip().strip(split))

    return retVal
def getPageWordSet(page):
    """
    Returns word set used in page content

    >>> sorted(getPageWordSet(u'<html><title>foobar</title><body>test</body></html>'))
    [u'foobar', u'test']
    """

    retVal = set()

    # only if the page's charset has been successfully identified
    if isinstance(page, unicode):
        _ = getFilteredPageContent(page)
        retVal = set(re.findall(r"\w+", _))

    return retVal
def htmlunescape(value):
    """
    Returns (basic conversion) HTML unescaped value

    >>> htmlunescape('a&lt;b')
    'a<b'
    """

    retVal = value
    if value and isinstance(value, basestring):
        codes = (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&nbsp;', ' '), ('&amp;', '&'))
        retVal = reduce(lambda x, y: x.replace(y[0], y[1]), codes, retVal)
        try:
            retVal = re.sub(r"&#x([^ ;]+);", lambda match: unichr(int(match.group(1), 16)), retVal)
        except ValueError:
            pass
    return retVal

def showStaticWords(firstPage, secondPage):
    """
    Prints words appearing in two different response pages
    """
    firstPage = getFilteredPageContent(firstPage)
    secondPage = getFilteredPageContent(secondPage)

    match = SequenceMatcher(None, firstPage, secondPage).ratio()
    print match
        
# text1_lines = requests.get("http://ccee.myvtc.edu.cn/asp\mod3list.aspx?mod=1&submod=50&type=1 and 1=2").text
# text2_lines = requests.get("http://ccee.myvtc.edu.cn/asp\mod3list.aspx?mod=1&submod=50&type=1").text
# showStaticWords(text1_lines,text2_lines)
print 1 > 0.8 > 0.4