# -*- coding: utf-8 -*-
import scrapy
from freebuf.items import FreebufItem
from scrapy import Request


class FreebufspriderSpider(scrapy.Spider):
    name = 'freebufSprider'
    allowed_domains = ['freebuf.com']
    start_urls = ['http://www.freebuf.com']
    cookie = {
        'acw_sc__': '5b860b5964470b6e528556c5c137be2837683b70',
    }

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie)

    def parse(self, response):
        # title = response.css('title::text').extract_first()
        for i in response.xpath("//div[@class='news_inner news-list']/div[@class='news-info']/dl"):
            yield {
                'title': i.xpath('dt/a/@title').extract_first(),
                'href': i.xpath('dt/a/@href').extract_first(),
                'author': i.xpath('dd/span[@class="name-head"]/a/@title').extract_first(),
                'time': i.xpath('dd/span[@class="time"]/text()').extract_first().strip(),
                'description': i.xpath('dd[@class="text"]/text()').extract_first().strip(),
            }
