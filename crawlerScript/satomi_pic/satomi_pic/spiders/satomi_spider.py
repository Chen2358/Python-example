from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from satomi_pic.items import SatomiPicItem

class SatomiSpider(CrawlSpider):

	name = 'satomi_pic_spider'

	download_delay = 1

	allowed_domains = []

	start_urls = [
		'http://movie.douban.com/celebrity/1016930/photo/1253599819/'
	]

	rules = (
		Rule(LinkExtractor(allow=(r'http://movie.douban.com/celebrity/1016930/photo/\d+/#photo')),
		callback='parse_item', follow=True),
	)

	def parse_item(self, response):
		print(response)

		sel = Selector(response)

		item = SatomiPicItem()
		item['image_urls'] = sel.xpath('//*[@id="content"]/div/div[1]/div[2]/div/a[1]/img/@src').extract()
		
		yield item