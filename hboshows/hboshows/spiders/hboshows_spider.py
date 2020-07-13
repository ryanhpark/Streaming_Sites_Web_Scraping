from hboshows.items import HboshowsItem
from scrapy import Spider, Request
import re

class HboshowsSpider(Spider):
	name = 'hboshows_spider'
	allowed_urls = ['https://reelgood.com']
	start_urls = ['https://reelgood.com/tv/source/hbo_max']

	def parse(self, response):
		result_urls = [f'https://reelgood.com/tv/source/hbo_max?offset={i}' for i in range(0,400,50)]

		for url in result_urls:
			yield Request(url=url, callback=self.parse_results_page)

	def parse_results_page(self, response):
		tvshow_urls = response.xpath('//td[@class="css-1u7zfla e126mwsw1"]/a/@href').extract()
		tvshow_urls = ['https://www.reelgood.com' + url for url in tvshow_urls]

		for url in tvshow_urls:
			yield Request(url=url, callback=self.parse_tvshow_page)

	def parse_tvshow_page(self, response):
		title = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
		imdb_score = response.xpath('//span[@class="css-xmin1q ey4ir3j3"]/text()').extract_first()
		rg_score = response.xpath('//span[@class="css-xmin1q ey4ir3j8"]/text()').extract_first()
		rated = response.xpath('//span[@title="Maturity rating"]/text()').extract_first().strip('Rated: ')
		seasons = re.findall('\d+', response.xpath('//span[@class="css-ee2w7g ey4ir3j1"]/text()').extract()[1])[0]
		year_start = re.findall('\d+',''.join(response.xpath('//span[@class="css-ee2w7g ey4ir3j1"]/a/text()').extract()))[0]
		year_end = response.xpath('//span[@class="css-ee2w7g ey4ir3j1"]/text()').extract_first().strip('- ')

		genres = response.xpath('//div[@class="css-19fr2c5"]/a/text()').extract()
		if genres == []:
			genres = response.xpath('//span[@class="css-ee2w7g ey4ir3j1"]/a/text()').extract()
			genres = ','.join(genres).split(year_start)[0].strip(',').lower()
		else:
			genres = ''.join(response.xpath('//div[@class="css-19fr2c5"]/a/@href').extract())
			if re.findall('/list', genres) == []:
				genres = ''.join(genres).split('/source')[0].split('/tv/genre/')
			elif re.findall('/source', genres) == []:
				genres = ''.join(genres).split('/list')[0].split('/tv/genre/')
			else:
				genres = ''.join(genres).split('/source')[0].split('/tv/genre/')
			genres = ','.join(genres[1:])

		item = HboshowsItem()
		item['title'] = title
		item['imdb_score'] = imdb_score
		item['rg_score'] = rg_score
		item['rated'] = rated
		item['seasons'] = seasons
		item['year_start'] = year_start
		item['year_end'] = year_end
		item['genres'] = genres
		item['resp_url'] = response.url
		item['resp_stat'] = response.status
		yield item


		


