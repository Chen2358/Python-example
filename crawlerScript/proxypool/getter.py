#-*- coding: utf-8 -*-
'''
分为：存储模块、获取模块、检测模块、接口模块

'''

    
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import *
import sys

#动态调用以crawl开头的方法并加入到数据库中
class Getter(object):

	def __init__(self):
		self.redis = RedisClient()
		self.crawler = Crawler()

	def is_over_threshold(self):
		"""
        判断是否达到了代理池限制
        """
		if self.redis.count() > = POOL_UPPER_THRESHOLD:
			return True
		else:
			return False

	def run(self):
		print('获取器开始执行')
		if not self.is_over_threshold():
			for callback_label in range(self.crawler.__CrawlFuncCount__):
				callback = self.crawler.__CrawlFunc__[callback_label]
				proxies = self.crawler.get_proxies(callback)
				for proxy in proxies:
					self.redis.add(proxy)