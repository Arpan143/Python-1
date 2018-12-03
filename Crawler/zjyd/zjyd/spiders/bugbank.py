# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pymongo
import logging
from zjyd.items import ZjydItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

class BugbankSpider(scrapy.Spider):
    name = 'bugbank'
    allowed_domains = ['bugbank.cn']
    # custom_settings = {
    #     'ITEM_PIPELINES':{
    #         'zjyd.pipelines.MongodbPipeline':300,
    #     }
    # }

    def start_requests(self):
        keywords = list(settings['KEYWORDS'])
        for i in keywords:
            url =  'https://www.bugbank.cn/api/tweets/search?keywords={}&page=1'.format(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ZjydItem()
        html = json.loads(response.text)
        if html['data']:
            page = int(response.url[response.url.find('page=') + 5]) + 1
            next_page = response.url[:response.url.find('page=') + 5] + str(page)
        else:
            next_page = None
        for data in html["data"]:
            if data["create_at"][:10] == time.strftime("%Y-%m-%d").decode('utf-8'):
                item['source'] = 'bugbank'
                item['title'] = data['data']['post']['title']
                item['url'] = u"https://www.bugbank.cn/q/article/" + data['_id'] + u".html"
                item['content'] = data["data"]["post"]["summary"]
                item['author'] = data['data']['post']['title']
                item['time'] = data["create_at"][:10]
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
        self.log("Bugbank sprider:%s" % (response.url))
