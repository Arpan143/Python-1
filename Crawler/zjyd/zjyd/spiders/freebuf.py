# -*- coding: utf-8 -*-
import scrapy
import time
import json
import logging
from zjyd.items import ZjydItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class FreebufSpider(scrapy.Spider):
    name = 'freebuf'
    allowed_domains = ['freebuf.com']
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'zjyd.pipelines.MongodbPipeline': 300,
    #     }
    # }

    def start_requests(self):
        keywords = list(settings['KEYWORDS'])
        for i in keywords:
            yield scrapy.Request(url=('https://search.freebuf.com/search/find/?year=0&score=0&articleType=0&origin=0&tabType=1&content=%s&page=1' % (i)), callback=self.parse)

    def parse(self, response):
        item = ZjydItem()
        data = json.loads(response.body_as_unicode())
        if data["data"]["total"] == u"0" or data["data"]["total"] == u"1":
                next_page = None
        else:
            page = int(response.url[response.url.find('page=') + 5:]) + 1
            next_page = response.url[:response.url.find('page=') + 5] + str(page)
        if data["data"]["total"] != u'0':
            for i in data["data"]["list"]:
                if i["time"] == time.strftime("%Y-%m-%d").decode('utf-8'):
                    item['source'] = 'freebuf'
                    item['title'] = i["title"]
                    item['url'] = i['url']
                    item['content'] = i['content']
                    item['time'] = i['time']
                    item['author'] = i['name']
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
        self.log("Freebuf sprider:%s" % (response.url))
