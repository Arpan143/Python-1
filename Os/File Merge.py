#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import argparse
# import re


def file_merge():
    print '''
 _        _   _      _  _    __    _  __________  _           _
| |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
| |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
|  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
| |      | |    \  /   | |_| || |_| || |         | |         | |
| |      | |    |  |    \   /  \   / | |________ | |________ | |________
|_|      |_|    |__|     \_/    \_/  |__________||__________||__________|
'''
    parser = argparse.ArgumentParser(description='File Merge')
    parser.add_argument('-n', dest='TARGET_num', required=True, help='File num')
    args = parser.parse_args()
    for i in range(args.TARGET_num):  # 循环读取多少文件
        f = open(str(i), 'r')  # 打开文件 r 是读取文件
        lines = f.readlines()  # 将文件以列表形式保存在lines里面
        lines1 = lines[-2:-1]
        lines2 = []  # 新建一个lines2列表
        lines2.extend(lines1)  # 向lines2里面添加lines1|extend等于列表间追加的意思,向lines2里面添加lines1
        h = open(r"result.txt", 'a')  # 以追加模式打开文件result.txt
        h.writelines(lines2)  # 向result.txt写入列表
        h.close()
        f.close()


if __name__ == '__main__':
    file_merge()
