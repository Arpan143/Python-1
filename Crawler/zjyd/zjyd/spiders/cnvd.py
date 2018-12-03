# -*- coding: utf-8 -*-
import scrapy
import time
import logging
from zjyd.items import ZjydItem
from scrapy.utils.project import get_project_settings

settings = get_project_settings()



class CnvdSpider(scrapy.Spider):
    name = 'cnvd'
    allowed_domains = ['cnvd.org.cn']

    def start_requests(self):
        keywords = list(settings['KEYWORDS'])
        for i in keywords:
            yield scrapy.Request(url=('http://www.cnvd.org.cn/flaw/list.htm?flag=true&keyword=%s&offset=0' %(i)), callback=self.parse)
      

    def parse(self, response):
        item = ZjydItem()
        if response.xpath("//table[@class='tlist']/div/tbody/tr/td[@colspan='5']/text()").extract_first() == u'对不起，没有找到相关的漏洞':
            next_page = None
        else:
            page = int(response.url[response.url.find('offset=') + 7:]) + 20
            next_page = response.url[:response.url.find('offset=') + 7] + str(page)
            for i in response.xpath("//table[@class='tlist']/div/tbody/tr"):
                if i.xpath("td[@width='13%' and not(@style)]/text()").extract_first().strip() == time.strftime("%Y-%m-%d").decode('utf-8'):
                    item['source'] = 'cnvd'
                    item['title'] = i.xpath("td[@width='45%']/a[@title]/@title").extract_first()
                    item['url'] = 'http://www.cnvd.org.cn' + i.xpath("td[@width='45%']/a/@href").extract_first()
                    item['time'] = i.xpath("td[@width='13%' and not(@style)]/text()").extract_first().strip()
                    item['author'] = u''
                    item['content'] = u''
                else:
                    next_page = None
                    continue
        logging.info(next_page)
        yield item
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        self.log("cnvd sprider:%s" % (response.url))
