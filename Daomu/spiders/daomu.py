# -*- coding: utf-8 -*-
import scrapy
from ..items import DaomuItem

class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    def parse(self, response):
        li_list=response.xpath('//li[contains(@id,"menu-item-20")]/a')
        for li in li_list:
            item=DaomuItem()
            item['title']=li.xpath('./text()').get()
            link=li.xpath('./@href').get()
            yield scrapy.Request(
                url=link,
                meta={'item':item},
                callback=self.parse_two_page
            )

    def parse_two_page(self,response):
        item=response.meta['item']
        article_list=response.xpath('//article')
        for article in article_list:
            name=article.xpath('./a/text()').get()
            two_link=article.xpath('./a/@href').get()
            yield scrapy.Request(
                url=two_link,
                meta={'item':item,'name':name},
                callback=self.parse_three_page
            )

    def parse_three_page(self,response):
        item=response.meta['item']
        item['name']=response.meta['name']
        content_list=response.xpath('//article[@class="article-content"]//p/text()').extract()
        item['content']='\n'.join(content_list)
        yield item









