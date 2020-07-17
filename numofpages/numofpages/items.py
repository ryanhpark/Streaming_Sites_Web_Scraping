# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NumofpagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pages = scrapy.Field()
    web_name = scrapy.Field()