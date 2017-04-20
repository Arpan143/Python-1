# coding=utf-8

import sys
import time
import telnetlib

with open('Smtp-data', 'rb') as f:
    str_1 = f.read()
    str_list = str_1.split('###!')
tn = telnetlib.Telnet(sys.argv[1], port=25, timeout=20)
time.sleep(1)
print tn.read_very_eager()
pdata = ''
for i in str_list:
    # if 'Subject' in i:
    pdata = i
    tn.write(pdata)
    print tn.read_very_eager()
    time.sleep(1)
