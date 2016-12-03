#!/usr/bin/env python
#coding:utf-8
import time,os

class hexcl:
    def __init__(self,path):
        self.path =path
        self.hexdict ={} #存放以两字节为一单位的字典,用于判断出现频率
        self.filename_list =[]
        self.h =open('result.txt','w+')
    def Get_filename(self):
        for root, dirs, files in os.walk(self.path):
            for i in range(len(files)):
                filename = str(root) + '/' + files[i]
                filename = filename.replace('\\','/')
                self.filename_list.append(filename)
    def hex_print(self):
        for g in self.filename_list:
            f = open(g,'rb')
            filelen = f.read()
            f.seek(0,0) #移动文件读取指针到指定位置
            lennum = len(filelen)/3 #文件长度的1/3
            byte = f.read(2) #先读取两个字节
            hexstr =  "%s" % byte.encode('hex') #得到hexstr
            if hexstr == '4d5a': #判断文件头,可自定义
                byte = f.read(lennum) #从文件lennum位置开始读取
                while True:
                    byte = f.read(32) #每次读取32个字节
                    hexstr =  "%s" % byte.encode('hex')
                    # print hexstr
                    y = 0
                    for i in range(32): #以两字节为一单位,得到字典
                        hex_2 = hexstr[y:y+2]
                        y = y+2
                        # print hex_2
                        if hex_2 !=None:
                            if hex_2 in self.hexdict:
                            # print hex_2
                                self.hexdict[hex_2] = self.hexdict[hex_2]+1
                            else:
                                self.hexdict[hex_2] = 1
                    if int(max(self.hexdict.items(), key=lambda x: x[1])[1])<5:
                        self.h.write(g+':'+hexstr+'\n')
                        break
                    else:
                        self.hexdict = {}
                        byte = ''
                        y = 0

def main():
    print '''
 _        _   _      _  _    __    _  __________  _           _
| |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
| |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
|  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
| |      | |    \  /   | |_| || |_| || |         | |         | |
| |      | |    |  |    \   /  \   / | |________ | |________ | |________
|_|      |_|    |__|     \_/    \_/  |__________||__________||__________|
'''
    Result =hexcl(r'C:\Users\Administrator\Desktop\xxx\1')
    Result.Get_filename()
    Result.hex_print()

if __name__ == '__main__':
    main()