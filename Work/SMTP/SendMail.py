# coding=utf-8
# -*- encoding: gb2312 -*-
import Send_config
import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header
import sqlite3
import re, codecs, sys


class Send_Mail():
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        # self.Content =Send_config.content
        self.Subject = Send_config.mail_title
        self.From = Send_config.sender
        self.To = ";".join(Send_config.receiver)
        self.connect = [Send_config.email_config[0], Send_config.email_config[1], Send_config.email_config[2]]

    def db_select(self):  # 读取工作内容
        print 'Today is ' + str(datetime.date.today())
        select_date = raw_input('When do you want to select?(xxxx-xx-xx)')
        cur.execute('select message from send_mail where date= "%s"' % (select_date))
        select_result = cur.fetchall()
        Work_str = select_result[0]
        print Work_str

    def db_write(self):  # 写入工作内容
        today_date = str(datetime.date.today())
        cur.execute('''INSERT INTO send_mail(date,message) VALUES ('%s','%s')''' % (today_date, self.Content))
        conn.commit()

    def get_work_content(self):
        f = codecs.open('work.txt', 'r', 'GBK')
        worklist = f.readlines()
        today_work1 = worklist[1]
        today_work2 = worklist[2]
        tomorrow_work = worklist[4]
        today_work1 = today_work1.encode("utf-8")
        today_work2 = today_work2.encode("utf-8")
        tomorrow_work = tomorrow_work.encode("utf-8")
        self.Content = Send_config.front_code + str(
            datetime.date.today()) + Send_config.front_code1 + today_work1 + Send_config.front_code2 + today_work2 + Send_config.front_code3 + tomorrow_work + Send_config.front_code4 + Send_config.front_code5

    def send_mail(self):  # 发送邮件
        message = MIMEText(self.Content, _subtype='html', _charset='utf-8')  # html为html格式邮件，text是附件形式
        message['Subject'] = self.Subject  # 设置邮件主题
        message['From'] = self.From  # 发件人
        message['To'] = self.To  # 收件人
        server = smtplib.SMTP()
        try:
            server.connect(self.connect[0])  # 连接服务器
            server.login(self.connect[1], self.connect[2])  # 登录
            server.sendmail(Send_config.sender, Send_config.receiver, message.as_string())
            server.close()
            return True
        except Exception , e:
            print Exception


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
    conn = sqlite3.connect(r'sendmail.db')
    cur = conn.cursor()
    success = Send_Mail(conn, cur)
    success.get_work_content()
    if success.send_mail():
        print "success"
    else:
        print "error"
    # success.db_write()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
