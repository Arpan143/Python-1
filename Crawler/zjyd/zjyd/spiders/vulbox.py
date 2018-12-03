# -*- coding: utf-8 -*-
import scrapy
import time
import logging
from zjyd.items import ZjydItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class VulboxSpider(scrapy.Spider):
    name = 'vulbox'
    allowed_domains = ['vulbox.com']
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'zjyd.pipelines.MongodbPipeline': 300,
    #     }
    # }

    def start_requests(self):
        keywords = list(settings['KEYWORDS'])
        for i in keywords:
            yield scrapy.Request(url=('https://www.vulbox.com/board/search/q/%s/page/1' % (i)), callback=self.parse)

    def parse(self, response):
        item = ZjydItem()
        if response.xpath("//div[@class='blackboard-list1']/div[@class='board-item1 clearfix']/div[@class='desc-inner']"):
            page = int(response.url[response.url.find('page/')+ 5:]) + 1
            next_page = response.url[:response.url.find('page/') + 5] + str(page)
        else:
            next_page = None
        for i in response.xpath("//div[@class='blackboard-list1']/div[@class='board-item1 clearfix']/div[@class='desc-inner']"):
            if i.xpath("div[@class='desc-date']/text()").extract_first().strip()[:-6] == time.strftime("%Y-%m-%d").decode('utf-8'):
                item['source'] = 'vulbox'
                item['title'] = i.xpath("div[@class='desc-info']/div[@class='desc-tit']/a/text()").extract_first()
                if i.xpath("div[@class='desc-info']/div[@class='desc-tit']/a/@href").extract_first() == u'javascript:;':
                    item['url'] = u'权限控制,无法查看'
                else:
                    item['url'] = 'https://www.vulbox.com' + i.xpath("div[@class='desc-info']/div[@class='desc-tit']/a/@href").extract_first()
                item['content'] = u'漏洞系统:' + i.xpath("div[@class='desc-info']/ul/li/a[@class='desc-comp']/text()").extract_first()
                item['time'] = i.xpath("div[@class='desc-date']/text()").extract_first().strip()
                item['author'] = i.xpath("div[@class='desc-info']/ul/li/a[@class='desc-user']/text()")
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
        self.log("Vulbox sprider:%s" % (response.url))
