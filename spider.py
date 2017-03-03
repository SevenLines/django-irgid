from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

DOMAIN = '83.220.170.91'
URL = 'http://%s:8086' % DOMAIN

class MySpider(BaseSpider):
    name = DOMAIN
    allowed_domains = [DOMAIN]
    start_urls = [
        URL
    ]

    def parse(self, response):
        if response.status != 200:
            print response.url
        le = LinkExtractor()  # empty for getting everything, check different options on documentation
        for link in le.extract_links(response):
            yield Request(link.url, callback=self.parse)