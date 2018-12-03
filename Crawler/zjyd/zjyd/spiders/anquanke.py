# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pymongo
import logging
from zjyd.items import ZjydItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class AnquankeSpider(scrapy.Spider):
    name = 'anquanke'
    allowed_domains = ['anquanke.com']
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'zjyd.pipelines.MongodbPipeline': 300,
    #     }
    # }

    def start_requests(self):
        keywords = list(settings['KEYWORDS'])
        for i in keywords:
            yield scrapy.Request(url=('https://api.anquanke.com/data/v1/search?size=20&s=%s&page=1' % (i)), callback=self.parse)   

    def parse(self, response):
        item = ZjydItem()
        data = json.loads(response.body_as_unicode())
        if data["total_count"] != u'0':
            if data['total_count'] == u'0' or data['total_count'] == u'1':
                next_page = None
            else:
                next_page = data['next']
            for i in data["data"]:
                if i["date"][:10] == time.strftime("%Y-%m-%d").decode('utf-8'):
                    item['source'] = 'anquanke'
                    item['title'] = i["title"]
                    item['url'] = u"https://www.anquanke.com/post/id/" + i['id']
                    item['content'] = i['content']
                    item['time'] = i["date"][:10]
                    item['author'] = u'null'
                else:
                    next_page = None
                    continue
        if item:
            yield item
        else:
            logging.info('%s is none!' % (response.url))
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        self.log("anquanke sprider:%s" % (response.url))
