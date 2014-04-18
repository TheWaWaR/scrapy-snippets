# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from unity3d.items import TopicItem, VideoItem


class VideoSpider(CrawlSpider):
    name = 'tutorials'
    start_urls = ['http://unity3d.com/learn/tutorials/modules/beginner']
    # rules = []

    def parse(self, response):
        sel = Selector(response)
        topics = [ TopicItem(title, descr)
                   for title, descr
                   in zip(sel.css('.pa20 h1.mb0').xpath('text()').extract(),
                          sel.css('.pt10.mb0').xpath('text()').extract())]
        print topics
        
