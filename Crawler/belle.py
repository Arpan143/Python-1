#!/usr/bin/env python
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
from multiprocessing import Process,Queue,Pool
import multiprocessing
import time
import random


def read_img_url(q):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' +
                             ' Chrome/55.0.2883.75 Safari/537.36'}
    for i in range(100):
        soup = BeautifulSoup(requests.get(raw_input(u'请输入url:'.encode('gbk')), headers=headers).text, 'lxml')#https://belle.la/page_' + str(i) + '/'
        for y in soup.find_all('img'):
            img_url = y.get('src')
            img_name = y.get('alt')
            if type(img_name) == unicode:
                try:
                    img_name = img_name.encode('gbk')
                except:
                    print img_name
                    img_name = img_name.encode('utf-8')
            else:
                pass
            q.put([img_name, img_url], block=False)
    q.put('Pleace End!')


def save_img(q):
    print 'Going!'
    while True:
        if not q.empty():
            img_list = q.get(False)
            if img_list == 'Pleace End!':
                break
            else:
                with open(r'.\Download\{}.{}'.format(img_list[0], img_list[1][len(img_list[1])-3: len(img_list[1])]), 'wb+') as img_hex:
                        img_hex.write(requests.get(img_list[1]).content)
                time.sleep(random.random())
        else:
            pass
    print "Ending!"


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
    manager = multiprocessing.Manager()
    q = manager.Queue()
    # lock = manager.Lock()
    read_img_url(q)
    p = Pool(processes=20)
    pr = p.apply_async(save_img, (q,))
    p.close()
    p.join()

if __name__ == '__main__':
    main()
