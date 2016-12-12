#!/usr/bin/env python
# -*-coding:utf-8-*-
import base64
from bs4 import BeautifulSoup
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
           , 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Upgrade-Insecure-Requests': '1'
          }
f = open(u'链接.txt', 'w+')
get_url = raw_input('请输入url:')
for i in range(int(raw_input('你要爬几页:'))):
    soup = BeautifulSoup(requests.get(get_url + '?page=' + str(i), headers=headers).text, 'lxml')
    for y in soup.find_all('p'):
        print base64.decodestring(y.string).decode('unicode-escape')
        f.write(base64.decodestring(y.string).decode('unicode-escape').encode('utf-8') + '\n')
