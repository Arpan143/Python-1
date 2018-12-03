# -*- coding: utf-8 -*-

# import os
import time
import pymongo
import scrapy
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import spiderloader

settings = get_project_settings()


def send_mail():
    mongo_client = pymongo.MongoClient(host=settings["MONGODB_HOST"], port=settings["MONGODB_PORT"])
    mongo_db = mongo_client[settings["MONGODB_DBNAME"]]
    mongo_query = {'time': time.strftime("%Y-%m-%d").decode('utf-8')}
    result = "邮件更新提醒:\n"
    
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    for i in spiders:
        mongo_col = mongo_db[i]
        if mongo_col.find(mongo_query).sort("ts",pymongo.ASCENDING).count() != 0:
            result += '%s 有更新,请注意查收!\n' % (i)
        else:
            result += '%s无更新!\n' % (i)

    sender = settings["MAIL_SENDER"]
    receivers = settings["MAIL_RECEIVERS"]

    message = MIMEText(result,'plain','utf-8')
    message['From'] = Header("hywell", 'utf-8')
    message['To'] = receivers
    subject = "信息收集爬虫"
    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP() 
    smtpObj.connect(settings["MAIL_HOST"], 25)
    smtpObj.login(settings["MAIL_USER"], settings["MAIL_PASSWORD"]) 
    smtpObj.sendmail(sender, receivers, message.as_string())

    mongo_client.close()

def main():
    # os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'zjyd.settings')
    process = CrawlerProcess(settings)
    # process.crawl('freebuf', domain='freebuf.com')
    # process.crawl('vulbox', domain='vulbox.com')
    # process.crawl('anquanke', domain='anquanke.com')
    # process.crawl('bugbank', domain='bugbank.com')
    # process.crawl('seebug', domain='seebug.com')
    # process.crawl('cnvd', domain='cnvd.org.cn')
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    classes = [spider_loader.load(name) for name in spiders]
    for i in classes:
        process.crawl(i)

    process.start()
    send_mail()

if __name__ == "__main__":
    main()
