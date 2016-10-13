#!/usr/bin/env python
# coding=utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
os.system("cmd /c dir") 
##系统信息 os.system('systeminfo') #os.popen()
##查看系统体系结构（32|64）：echo %PROCESSOR_ARCHITECTURE%
#查看环境变量：set
#查看路由表信息：route print
#查看ARP缓存信息：ARP -A
##查看活动的链接：netstat -ano
#查看防火墙：netsh advfirewall
#查看计划任务：schtasks
#查看安装的驱动：DRIVERQUERY 
##查看服务进程ID：tasklist
##查看可读可写的文件夹:dir /a-r-d /s /b