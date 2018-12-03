# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pymysql
import smtplib
import logging
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class ZjydPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        pass


class MysqlPipeline(object):
    def __init__(self):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            port = settings['MYSQL_PORT'],
            dbname = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    def process_item(self, item, spider):
            query = self.dbpool.runInteraction(self.do_insert, item, spider)
            logging.info('MySQL connect')
            query.addErrback(self.handle_error, item, spider)
            query.addBoth(lambda _: item)
            return query
    
    def handle_error(self, failure, item, spider):
        print failure

    def do_insert(self, cursor, item):
        cursor.execute("insert into zjyd (title, url, content, time, author, source) values(%s, %s, %s, %s, %s, %s)",
                        item['title'], item['url'], item['content'], item['time'], item['author'], item['source'])

class MongodbPipeline(object):
    def __init__(self):
        self.mongo_host = settings["MONGODB_HOST"]
        self.mongo_port = settings["MONGODB_PORT"]
        self.mongo_db = settings["MONGODB_DBNAME"]

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        info = dict(item)
        self.db[item['source']].insert_one(info)
        return item
