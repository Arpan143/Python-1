#!/usr/bin/env python
# coding=utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
os.system("cmd /c dir") 
##ϵͳ��Ϣ os.system('systeminfo') #os.popen()
##�鿴ϵͳ��ϵ�ṹ��32|64����echo %PROCESSOR_ARCHITECTURE%
#�鿴����������set
#�鿴·�ɱ���Ϣ��route print
#�鿴ARP������Ϣ��ARP -A
##�鿴������ӣ�netstat -ano
#�鿴����ǽ��netsh advfirewall
#�鿴�ƻ�����schtasks
#�鿴��װ��������DRIVERQUERY 
##�鿴�������ID��tasklist
##�鿴�ɶ���д���ļ���:dir /a-r-d /s /b