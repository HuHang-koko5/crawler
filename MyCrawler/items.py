# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class editorialItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    time_zone = scrapy.Field()
    content = scrapy.Field()


class dramaAddressItem(scrapy.Item):
    title = scrapy.Field()
    duration = scrapy.Field()
    href = scrapy.Field()


class subtitleItem(scrapy.Item):
    title = scrapy.Field()
    timeline = scrapy.Field()
    content = scrapy.Field()

class newsItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()

class newsContentItem(scrapy.Item):
    title = scrapy.Field()
    stand_first = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()





