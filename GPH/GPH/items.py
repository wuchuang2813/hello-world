# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GphItem(scrapy.Item):
    name = scrapy.Field()
    huohao = scrapy.Field()
    bianhao = scrapy.Field()
    huoqi = scrapy.Field()
    # price = scrapy.Field()
    pric = scrapy.Field()
    unit = scrapy.Field()
    xinghao = scrapy.Field()
    weight = scrapy.Field()
    bzsl = scrapy.Field()
