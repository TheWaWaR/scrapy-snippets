# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TopicItem(Item):
    title = Field()
    descr = Field()

    def __init__(self, title, descr):
        self['title'] = title
        self['descr'] = descr


class VideoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    topic = Field()
    level = Field()
    number = Field()
    url = Field()               # Original page, for reading scripts.
    title = Field()
    descr = Field()
    youtube_key = Field()

