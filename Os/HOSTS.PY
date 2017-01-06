# -*-coding:utf-8-*-
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' +
                         ' Chrome/55.0.2883.75 Safari/537.36'}
req = requests.get('https://raw.githubusercontent.com/racaljk/hosts/master/hosts', headers=headers, verify=False)
try:
    f = open(r'C:\Windows\System32\drivers\etc\HOSTS','w+')
    f.write(req.text)
    f.close()
except IOError as e:
    print e
    print u"权限不够".encode('gbk')