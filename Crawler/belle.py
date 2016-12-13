#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import threading
import time


def save_img(url_str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
               }
    soup = BeautifulSoup(requests.get('https://belle.la/page_' + str(url_str) + '/', headers=headers).text, 'lxml')
    for y in soup.find_all('img'):
        img_url = y.get('src')
        img_name = y.get('alt')
        if type(img_name) == unicode:
            img_name = img_name.encode('gbk')
        else:
            pass
        print img_url
        with open(r'F:\Download\{}.{}'.format(img_name, img_url[len(img_url)-3: len(img_url)]), 'wb+') as img_hex:
            img_hex.write(requests.get(img_url).content)
            time.sleep(2)


def main():
    threads = []
    saves = 20
    for i in range(saves):
        t = threading.Thread(target=save_img, args=[i])
        threads.append(t)
    for i in range(saves):
        threads[i].start()
    for i in range(saves):
        threads[i].join()

if __name__ == '__main__':
    main()
