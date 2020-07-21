from streamingsites.items import StreamingsitesItem
from scrapy import Spider, Request
import re

class StreamingsitesSpider(Spider):
	name = 'streamingsites_spider'
	allowed_domains = ['reelgood.com']
	start_urls = ['https://reelgood.com']

	def parse(self, response):

		hbo = [f'https://reelgood.com/source/hbo_max?offset={i}' for i in range(0,2150,50)]
		netflix = [f'https://reelgood.com/source/netflix?offset={i}' for i in range(0,5500,50)]
		hulu = [f'https://reelgood.com/source/hulu?offset={i}' for i in range(0,2700,50)]
		disney = [f'https://reelgood.com/source/disney_plus?offset={i}' for i in range(0,850,50)]
		amazon = [f'https://reelgood.com/source/amazon?offset={i}' for i in range(0,16250,50)]

		result_urls = hbo + netflix + hulu + disney + amazon
		
		for url in result_urls:
			yield Request(url=url, callback=self.parse_results_page, dont_filter = True)

	def parse_results_page(self, response):
		shows_urls = response.xpath('//td[@class="css-1u7zfla e126mwsw1"]/a/@href').extract()
		shows_urls = ['https://reelgood.com' + url for url in shows_urls]

		web_name = response.url.split('/')[-1].split('?')[0]
		meta = {'web_name': web_name}

		for url in shows_urls:
			yield Request(url=url, callback=self.parse_shows_page, meta = meta, dont_filter = True)

	def parse_shows_page(self, response):
		movie_or_tv = response.url.split('/')[-2]
		title = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
		imdb_score = response.xpath('//span[@class="css-xmin1q ey4ir3j3"]/text()').extract_first()
		rg_score = response.xpath('//span[@class="css-xmin1q ey4ir3j8"]/text()').extract_first()
		rated = response.xpath('//span[@title="Maturity rating"]/text()').extract()
		if rated != []:
			rated = rated[0].strip('Rated: ')
		else:
			rated = ""

		seasons = response.xpath('//span[@class="css-ee2w7g ey4ir3j1"]/text()').extract()
		if re.findall('eason', ''.join(seasons)) == []:
			seasons = ""
		else:
			seasons = re.findall('\d+', seasons[1])[0]
			

		year_start = re.findall('\d+',''.join(response.xpath('//span[@class="css-ee2w7g ey4ir3j1"]/a/text()').extract()))[0]

		year_end = response.xpath('//span[@class="css-ee2w7g ey4ir3j1"]/text()').extract_first().strip('- ')
		if year_end == "Present":
			year_end = 2020
		elif re.findall('m', year_end) != []:
			year_end = ""
		elif year_end == "On:":
			year_end = ""

		genres = response.xpath('//div[@class="css-19fr2c5"]/a/@href').extract()
		if (genres == []) | (re.findall('/genre', ''.join(genres)) == []) :
			genres = response.xpath('//span[@class="css-ee2w7g ey4ir3j1"]/a/text()').extract()
			genres = ','.join(genres).split(year_start)[0].strip(',').lower()
		else:
			genres = ''.join(genres)
			if re.findall('/movies/genre', genres) == []:
				if re.findall('/source', genres) == []:
					genres = ''.join(genres).split('/list')[0].split('/tv/genre/')
				else:
					genres = ''.join(genres).split('/source')[0].split('/tv/genre/')
			else:
				if re.findall('/source', genres) == []:
					genres = ''.join(genres).split('/list')[0].split('/movies/genre/')
				else:
					genres = ''.join(genres).split('/source')[0].split('/movies/genre/')
			genres = ','.join(genres[1:])
			if re.findall('/country', genres) != []:
				genres = genres.split('/country')[0]

		item = StreamingsitesItem()
		item['web_name'] = response.meta['web_name']
		item['movie_or_tv'] = movie_or_tv
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



