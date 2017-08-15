#!/usr/bin/env python
# coding=utf-8

import requests
import gevent
from gevent.queue import Queue
from bs4 import BeautifulSoup
import urllib
# import re


def work(entry_url):
    global inUrl
    global seUrl
    global ouUrl
    global urlQueue
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
    }
    r = requests.get(entry_url, verify=False, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    for y in soup.find_all('a'):
        url = y.get('href')
        if url is not None:
            if url.find(inUrl) != -1: #(url.find(inUrl) and url.find(ouUrl))
                if url.split('/')[-1].find('#') != -1:
                    url = url[:url.split('/')[-1].find('#')]
                if (url in seUrl) is False:
                    seUrl.add(url)
                    urlQueue.put(url)
            elif url[0] == '/':
                url = inUrl + url
                if url.split('/')[-1].find('#') != -1:
                    url = url[:url.split('/')[-1].find('#')]
                if (url in seUrl) is False:
                    seUrl.add(url)
                    urlQueue.put(url)


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
    global inUrl
    global ouUrl
    global urlQueue
    threads = []
    entry_url = raw_input('Place enter the entry url:')
    if entry_url.find('http') == -1:
        entry_url = 'http://' + entry_url
    inUrl = entry_url
    # pattern = re.compile(r'(?<=://)[a-zA-Z\.0-9]+') # 用于获取域名
    # domain = pattern.search(entry_url)
    # inUrl = domain.group()
    # if inUrl[0:4] == "www.":
    #     ouUrl = inUrl[4:]
    # else:
    #     ouUrl = inUrl
    #     inUrl = "www." + inUrl
    urlQueue.put(entry_url)
    while True:
        if not urlQueue.empty():
            url = urlQueue.get()
            if len(threads) < 100:
                threads.append(gevent.spawn(work, url))
            else:
                gevent.joinall(threads)
                threads = []
        else:
            if len(threads) > 0:
                gevent.joinall(threads)
                threads = []
            else:
                break

inUrl = "" # www.xxx.com
ouUrl = "" # xxx.com
seUrl = set()
urlQueue = Queue()
if __name__ == '__main__':
    main()
    for i in seUrl:
        print urllib.unquote(i)
