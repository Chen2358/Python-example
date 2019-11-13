# -*- coding: utf-8 -*-



import requests

#拼接好的图片集和列表路径
all_urls =  []

class Spider(object):

	def __init__(self, target_url, headers):
		self.target_url = target_url
		self.headers = headers

	#获取所有的想抓取的URL
	def getUrls(self, start_page, page_num):
		global all_urls
		for i in range(start_page, page_num+1):
			url = self.target_url % i
			all_urls.append(url)

if __name__ == '__main__':
	headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
			'HOST':'www.meizitu.com'
	}
	target_url = 'http://www.meizitu.com/a/pure_%d.html' #图片集和列表规则

	spider = Spider(target_url, headers)
	spider.getUrls(1, 16)
	print(all_urls)