#!/usr/bin/env python
# -*-coding:utf-8-*-
import base64
from bs4 import BeautifulSoup
import requests
import time


def xFuck():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.'
                             '2883.75 Safari/537.36', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
               'Upgrade-Insecure-Requests': '1'
               }
    f = open(u'链接.txt'.encode('gbk'), 'w+')
    get_url = raw_input(u'请输入url:'.encode('gbk')) #http://www.xfuck.cc/catalog.asp
    for i in range(1, int(raw_input(u'待爬取页数:'.encode('gbk')))):
        soup = BeautifulSoup(requests.get(get_url + '?page=' + str(i), headers=headers).text, 'lxml')
        for y in soup.find_all('p'):
            try:
                print y.string
                print base64.decodestring(y.string).decode('unicode-escape')
                time.sleep(10)
                f.write(base64.decodestring(y.string).decode('unicode-escape').encode('utf-8') + '\n')
            except UnicodeEncodeError:
                print u'解密失败'.encode('gbk')


def main():
    print """
     _        _   _      _  _    __    _  __________  _           _
    | |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
    | |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
    |  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
    | |      | |    \  /   | |_| || |_| || |         | |         | |
    | |      | |    |  |    \   /  \   / | |________ | |________ | |________
    |_|      |_|    |__|     \_/    \_/  |__________||__________||__________|

        """
    xFuck()
