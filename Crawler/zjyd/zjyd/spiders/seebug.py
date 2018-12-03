# -*- coding: utf-8 -*-
import scrapy
import time

from zjyd.items import ZjydItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class SeebugSpider(scrapy.Spider):
    name = 'seebug'
    allowed_domains = ['seebug.org']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'zjyd.pipelines.SeleniumMiddleware': 723,
        },
    }

    def start_requests(self):
        keywords = list(settings['KEYWORDS'])
        for i in keywords:
            yield scrapy.Request(url=('https://www.seebug.org/search/?keywords=%s&category=&page=1' % str(i)), callback=self.parse)

    def parse(self, response):
        item = ZjydItem()
        if response.xpath("//table[@class='table sebug-table table-vul-list']/tbody/tr"):
            page = int(response.url[response.url.find('page=') + 5]) + 1
            next_page = response.url[:response.url.find('page=') + 5] + str(page)
        else:
            next_page = None
        for i in response.xpath("//table[@class='table sebug-table table-vul-list']/tbody/tr"):
            if i.xpath("td[@class='text-center datetime hidden-sm hidden-xs']/text()").extract_first().strip()[:-6] == time.strftime("%Y-%m-%d").decode('utf-8'):
                item['source'] = 'seebug'
                item['title'] = i.xpath("td[@class='vul-title-wrapper']/a[@class='vul-title']/text()").extract_first()
                item['time'] = i.xpath("td[@class='text-center datetime hidden-sm hidden-xs']/text()").extract_first().strip()
                item['url'] = u'https://www.seebug.org' + i.xpath("td[@class='vul-title-wrapper']/a[@class='vul-title']/href").extract_first()
                item['content'] = i.xpath("td[@class='vul-title-wrapper']/a[@class='vul-title']/text()").extract_first()
                item['author'] = u'null'
            else:
                next_page = None
                continue
        if item:
            yield item
        else:
            self.log('%s is none!' % (response.url))
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        self.log("seebug sprider:%s" % (response.url))
