from scrapy.spiders import Spider 
from scrapy.selector import Selector

class DmozSpider(Spider):

	name = "sogaa"
	allowed_domains = ["sogaa.net"]
	start_urls = ['http://www.sogaa.net/']

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath('/html/body/div[1]/div[3]/div/div/ul/li')
		items = []
		for site in sites:
			items = DmozItem()
			item['title'] = site.xpath('a/text()').extract()
			# item['title']  =  site.xpath('a/@href').extract()
			items.append(item)
		return items
		