#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy.item import Item, Field
from scrapy.contrib.spiders import CrawlSpider, Rule

class VideoItem(Item):
    pass


class Unity3DTutorialSpider(CrawlSpider):
    name = 'unity3d-tutorials'
    start_urls = ['http://unity3d.com/learn/tutorials/modules/beginner']
    rules = []


