from numofpages.items import NumofpagesItem
from scrapy import Spider, Request
import re

class NumofpagesSpider(Spider):
	name = 'numofpages_spider'
	allowed_domains = ['reelgood.com']
	start_urls = ['https://reelgood.com']

	def parse(self, response):

		hbo = [f'https://reelgood.com/source/hbo_max?offset={i}' for i in range(0,3000,50)]
		netflix = [f'https://reelgood.com/source/netflix?offset={i}' for i in range(0,6000,50)]
		hulu = [f'https://reelgood.com/source/hulu?offset={i}' for i in range(0,3000,50)]
		disney = [f'https://reelgood.com/source/disney_plus?offset={i}' for i in range(0,1000,50)]
		amazon = [f'https://reelgood.com/source/amazon?offset={i}' for i in range(0,17000,50)]

		result_urls = hbo + netflix + hulu + disney + amazon
		
		for url in result_urls:
			yield Request(url=url, callback=self.parse_results_page, dont_filter = True)

	def parse_results_page(self, response):
		
		web_name = response.url.split('/')[-1].split('?')[0]
		
		pages = response.xpath('//button[@class="css-qbp45y eyx6tna2"]//text()').extract()
		if pages != []:
			pages = 50
		else:
			pages = 0

		item = NumofpagesItem()
		item['web_name'] = web_name
		item['pages'] = pages
		yield item