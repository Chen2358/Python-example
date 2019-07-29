#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector

from douban_new_movie.items import DoubanNewMovieItem

class DoubanNewMovieSpdier(Spider):

	name = 'douban_new_movie_spider'

	allowed_domains = ['https://movie.douban.com']

	start_urls = [
	'http://movie.douban.com/chart'
	]

	def parse(self, response):
		sel = Selector(response)

		movie_name = sel.xpath('//*[@id="screening"]/div[2]/ul/li[6]/ul/li[2]/a/text()').extract()
		movie_url =  sel.xpath('//*[@id="screening"]/div[2]/ul/li[6]/ul/li[2]/a/@href').extract()
		movie_star = sel.xpath('//*[@id="screening"]/div[2]/ul/li[6]/ul/li[3]/span[2]/text()').extract()

		item  = DoubanNewMovieItem()

		item['movie_name'] = [n.encode('utf-8') for n in movie_name]
		item['movie_star'] = [n for n in movie_star]
		item['movie_url'] = [n for n in movie_url]

		yield item

		print(movie_name, movie_star,movie_url)