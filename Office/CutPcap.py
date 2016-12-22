#!/usr/bin/env python
# coding=utf-8
import sys
import struct
import socket
import os
import binascii
import re


def write_pcap(pcap_header_string, tuple_info, file_name, pcap_dir):
    num = 0
    os.mkdir(pcap_dir + "\\" + file_name)
    for key in tuple_info:
        finap = open(pcap_dir + "\\" + file_name + "\\" + file_name + "-" + key + ".pcap", 'wb')
        finap.write(pcap_header_string + tuple_info[key])
        finap.close()
        num += 1


def read_pcap(filedir, pcap_dir):
    i = 24
    tuple_info = {}
    packet_num = 0
    fpcap = open(filedir, 'rb') #以二进制打开pcap文件
    string_data = fpcap.read() #读取
    file_middle_name = filedir.split("\\")[-1]
    file_name = file_middle_name.split(".")[0]
    pcap_header_string = string_data[0:24]  # pcap文件头
    y = 0
    while (i < len(string_data)):  # 第一次i=24 24个字节前面都是pcap的头部信息 固定长度
        pcap_packet_header = string_data[i:i + 16]  # 每个数据包头部信息
        pcap_packet_header_len = string_data[i + 12:i + 16]  # 数据包实际长度
        packet_len = struct.unpack('I', pcap_packet_header_len)[0]  # 通过struct将数据包实际长度解析为unsigned int型数据
        packet_value = string_data[i + 16:i + 16 + packet_len]  # 获取包的内容
        i = i + packet_len + 16 #固定加上数据包的长度和数据包头的长度
        ip_type = binascii.b2a_hex(packet_value[12:14])
        if ip_type == '86dd':  # 用来判断是否为ipv6的包
            sip = packet_value[22:38] #获取源地址十六进制
            sip_str = binascii.b2a_hex(sip[0:2]) + ':' + binascii.b2a_hex(sip[2:4]) + ':' + binascii.b2a_hex(
                sip[4:6]) + ':' + binascii.b2a_hex(sip[6:8]) + ':' + binascii.b2a_hex(
                sip[8:10]) + ':' + binascii.b2a_hex(sip[10:12]) + ':' + binascii.b2a_hex(
                sip[12:14]) + ':' + binascii.b2a_hex(sip[14:16]) #获取源地址字符串
            sip_str = sip_str.replace(':', '.')
            sip_str = re.sub('(?is)(0000\.)+', '.', sip_str) #正则替换
            sip_str = re.sub('(?is)(000)(?=\w)', '', sip_str) #正则替换
            sip_str = re.sub('(?is)(00)(?=\w)', '', sip_str) #正则替换
            sport = packet_value[54:56] #获取源端口十六进制
            sport_str = str(ord(sport[0]) * 256 + ord(sport[1])) #获取源端口字符串
            dip = packet_value[38:54] #获取目的地址十六进制
            dip_str = binascii.b2a_hex(dip[0:2]) + ':' + binascii.b2a_hex(dip[2:4]) + ':' + binascii.b2a_hex(
                dip[4:6]) + ':' + binascii.b2a_hex(dip[6:8]) + ':' + binascii.b2a_hex(
                dip[8:10]) + ':' + binascii.b2a_hex(dip[10:12]) + ':' + binascii.b2a_hex(
                dip[12:14]) + ':' + binascii.b2a_hex(dip[14:16]) #获取目的地址字符串
            dip_str = dip_str.replace(':', '.')
            dip_str = re.sub('(?is)(0000\.)+', '.', dip_str) #正则替换
            dip_str = re.sub('(?is)(000)(?=\w)+', '', dip_str) #正则替换
            dip_str = re.sub('(?is)(00)(?=\w)', '', dip_str) #正则替换
            dport = packet_value[56:58] #获取目的端口
            dport_str = str(ord(dport[0]) * 256 + ord(dport[1])) #获取目的端口字符串
            try:
                addr = socket.inet_pton(socket.AF_INET6, sip_str)
            except TypeError:
                pass
            tuple_string = sip_str + "_" + sport_str + "-" + dip_str + "_" + dport_str #以源地址端口到目的地址端口为字典
            tuple_contrary_string = dip_str.replace(':', '.') + "_" + dport_str + "-" + sip_str.replace(':',
                                                                                                        '.') + "_" + sport_str
            #以目的地址端口到源地址端口为字典
            if tuple_info.has_key(tuple_string):
                tuple_info[tuple_string] += pcap_packet_header + packet_value
            elif tuple_info.has_key(tuple_contrary_string):
                tuple_info[tuple_contrary_string] += pcap_packet_header + packet_value
            else:
                tuple_info[tuple_string] = pcap_packet_header + packet_value
    write_pcap(pcap_header_string, tuple_info, file_name, pcap_dir) #写


def is_contain_file(pcap_path):
    flag = 0
    for item in pcap_path:
        if item.endswith(".pcap"):
            flag = 1
            break
    return flag


def main():
    # print sys.argv #python cut_pcap.py pcaps :['cut_pcap.py', 'pcaps']
    # time.sleep(10)
    try:
        pcap_dir = sys.argv[1]
    except:
        print "Error! please input a parameter of the pcap directory!"
        sys.exit(1)  # 有错误退出
    if os.path.isdir(pcap_dir):  # 判断pcap_dir是否为目录
        files = os.listdir(pcap_dir)  # 获取pcap文件名
        if is_contain_file(files) == 1:  # 判断是否为pcap后缀
            for item in files:
                if item.endswith(".pcap"):
                    read_pcap(pcap_dir + "\\" + item, pcap_dir)
        else:
            print "Error! the directory does not contain any pcap file!"
            exit(1)
    elif pcap_dir.endswith(".pcap"):
        if os.path.exists(pcap_dir):
            read_pcap(pcap_dir, "\\".join(pcap_dir.split("\\")[:-1]))
        else:
            print "Error! the pcap is not exit please check it!"
            exit(1)
    else:
        print "Error! the directory is not true please check it!"
        sys.exit(1)


if __name__ == '__main__':
    main()
