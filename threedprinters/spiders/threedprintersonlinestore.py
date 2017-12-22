# -*- coding: utf-8 -*-
# pylint: disable-all
import scrapy
from scrapy.http import Request


class ThreedprintersonlinestoreSpider(scrapy.Spider):
    name = 'threedprintersonlinestore'
    allowed_domains = ['www.3dprintersonlinestore.com']
    start_urls = ['https://www.3dprintersonlinestore.com/3d-printers?page=2',
                  'http://www.3dprintersonlinestore.com/3d-printers/']

    def parse(self, response):
        for href in response.css('.product__inside .product__inside__name a::attr(href)').extract():
            yield Request(url=href, callback=self.parseIndividualPage)
        pass

    def parseIndividualPage(self, response):
        specs = ''
        for row in response.css('.table.table-params tr'):
            count = 0
            for col in row.css('td:not([colspan="2"])::text').extract():
                specs += col
                count += 1
                if count == 1:
                    specs += ': '
            specs += '\n'
        yield {
            'url': response.url,
            'name': response.css('.product-info__title h1::text').extract_first(),
            'normal_price': response.css('.product-info__price .price-box__old::text').extract_first() or response.css('.product-info__price .price-regular::text').extract_first(),
            'discounted_price': response.css('.product-info__price .price-box__new::text').extract_first(),
            'specs': specs
        }
