# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' +
                         ' Chrome/55.0.2883.75 Safari/537.36'}
result = ''
for i in range(25):
    i += 1
    req = requests.get('http://bbs.kafan.cn/forum-31-'+str(i)+'.html', headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    for y in soup.find_all('a'):
        try:
            if y.string[0:4] == u'精睿样本':
                result += y.string + ':' + y['href'] + '\n'
        except KeyError as e:
            pass
        except TypeError as e:
            pass
f = open('result.txt', 'w+')
f.write(result.encode('utf-8'))
f.close()
