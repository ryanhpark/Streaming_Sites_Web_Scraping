# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StreamingsitesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	movie_or_tv = scrapy.Field()
	title = scrapy.Field()
	imdb_score = scrapy.Field()
	rg_score = scrapy.Field()
	rated = scrapy.Field()
	genres = scrapy.Field()
	seasons = scrapy.Field()
	year_start = scrapy.Field()
	year_end = scrapy.Field()
	resp_url = scrapy.Field()
	resp_stat = scrapy.Field()
	web_name = scrapy.Field()
