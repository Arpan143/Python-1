#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import regex
from multiprocessing import Process,Queue,Pool
import multiprocessing
import time
import random


def login(url_info):
    headers = url_info['headers']
    username = url_info['username']
    password = url_info['password']
    login_url = url_info['login_url']
    post_data = {
        'email': (None, username),
        'password': (None, password)
            } #multipart form data
    session = requests.Session()
    session.post(login_url, data=post_data, headers=headers, verify=False)
    print 'Login'
    time.sleep(random.random())
    return session


def get_page_num(url_info):
    page_list = [i for i in range(10000)]
    page_min = 1
    page_max = len(page_list)
    html_url = url_info['html_url']
    headers = url_info['headers']
    while page_min < page_max:
        mid = (page_min + page_max) / 2
        page_html = requests.get(html_url + str(mid), headers=headers, verify=False).text
        time.sleep(random.random())
        if u'无结果' in page_html:
            page_max = mid
        else:
            page_min = mid
        if page_max - page_min == 1:
            print page_min
            return page_min


def read_html(url_info, read_queue, down_queue):
    while True:
        if not read_queue.empty():
            time.sleep(random.random())
            file_info = {} #key为哈希 键值为列表：名字、危害级别、下载链接
            hosts = url_info['hosts']
            session = url_info['session']
            headers = url_info['headers']
            re_sample = '(?<=<a\shref=")/sample/.*?(?=")' #样本的url正则
            re_down = '(?<=<a\shref=")/download-sample/.*?(?=")'  # 样本下载的url正则
            read_url = read_queue.get()
            html_read = session.get(read_url, headers=headers, verify=False).text #忽略SSL证书
            url_sample = regex.findall(re_sample, html_read) #样本的url列表
            for y in url_sample:
                hash_string = y[8:-18]
                re_name = ur'(?<=[输入|Input]</dt>\s+.*\s+.*<b>)\b\w.*(?=</b>\s+.+' + hash_string + ')' #获取名字的正则
                re_level = '(?<=' + hash_string + ur'</span></dd>\s+.+[威胁级别|Threat level]</dt>\s+<dd>\s+<span\s.*>\s*)\b\w.*(?=</span>|\s+</span>)'  # 危害等级的正则
                try:
                    input_name = regex.search(re_name, html_read).group() #获取名字
                except AttributeError:
                    input_name = 'No name'
                try:
                    thread_level = regex.search(re_level, html_read).group()  # 获取危害等级
                except AttributeError:
                    thread_level = 'No thread_level'
                file_info[hash_string] = [input_name, thread_level] #写入字典
            url_down = regex.findall(re_down, html_read) #获取样本下载的url
            url_down = list(set(url_down)) #去重
            for i in url_down:
                hash_down = i[17:-18]
                down_url = hosts + i
                file_info[hash_down].append(down_url)
                down_queue.put([hash_down, file_info[hash_down][0], down_url], block=False)
        else:
            down_queue.put(['End', 'End', 'End'])
            break


def write_file(url_info, down_queue):
    session = url_info['session']
    headers = url_info['headers']
    # print 'String writing!'
    while True:
        if not down_queue.empty():
            time.sleep(5)
            down_info = down_queue.get(False)
            if down_info == 'End':
                break
            else:
                down_html = session.get(down_info[2], headers=headers, verify=False)
                if str(down_html.status_code)[0] == '4':
                    # print down_info[1]
                    pass
                else:
                    try:
                        with open('./file/' + down_info[1], "wb") as code:
                            code.write(down_html.content)
                            time.sleep(random.random())
                    except IOError:
                        with open('./file/' + down_info[0], "wb") as code:
                            code.write(down_html.content)
                            time.sleep(random.random())
        else:
            break


def write_result():
    # f = open('result.txt', 'w+')
    # for key in file_info:  # 将名字、危害程度输出至文件
    #     write_string = u'%s:%s:%s\n' % (key, file_info[key][0], file_info[key][1])
    #     write_string = write_string.encode('utf-8')
    #     f.write(write_string)
    # f.close()
    pass


def main():
    headers = {'Host': 'www.hybrid-analysis.com',
               'Connection': 'keep-alive',
               'Pragma': 'no-cache',
               'Cache-Control': 'no-cache',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
               }
    username = '' #待输入的用户名
    password = '' #待输入的密码
    url_info = {
        'hosts': 'https://www.hybrid-analysis.com',
        'html_url': 'https://www.hybrid-analysis.com/recent-submissions?filter=file&lang=zh&page=',
        'login_url': 'https://www.hybrid-analysis.com/login',
        'headers': headers,
        'username': username,
        'password': password
    } #设置爬取时所需要的数据：hosts、html、headers、username、password等
    page_num = get_page_num(url_info)
    url_info['session'] = login(url_info)
    manager = multiprocessing.Manager()
    read_queue = manager.Queue()
    down_queue = manager.Queue()
    down_list = []
    for i in range(page_num):
        i += 1
        down_list.append(url_info['html_url'] + str(i))
    for i in down_list:
        read_queue.put(i, block=False)
    read_process = Pool(processes=10)
    pr = read_process.apply_async(read_html, (url_info, read_queue, down_queue))
    down_process = Pool(processes=10)
    time.sleep(30)
    print "Writing start"
    pd = down_process.apply_async(write_file, (url_info, down_queue))
    down_process.close()
    down_process.join()


if __name__ == '__main__':
    main()
