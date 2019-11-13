#-*- coding: utf-8 -*-

'''
存储模块：Redis，
Hash的名称可做二级分类，如账号的Hash为，accounts:weibo
'''

 import random
 import redis
 from cookiespool.config import *

class RedisClient(object):

	def __int__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
		self.db = redis.StrictRedis(host=host, port=port, password=password, decode_response=True)
		self.type = type
		self.website = website

	def name(self):
		'''
		获取Hash的名称
		'''
		return "{type}:{website}".format(type=self.type, website=self.website)

	def set(self, username, value):
		'''
		设置键值对
		'''
		return self.db.hset(self.name(), username, value)

	def get(self, username):
		'''
		根据键名获取键值
		'''
		return self.db.hget(self.name(), username)

	def delete(self, username):
		'''
		根据键名删除键值对
		'''
		return self.db.hdel(self.name(), username)

	def count(self):
		'''
		获取数目
		'''
		return self.db.hlen(self.name())

	def random(self):
		'''
		随机得到键值，用于随机Cookies获取
		'''
		return random.choice(self.db.hvals(self.name()))

	def usernames(self):
		'''
		获取所有账户信息
		'''
		return self.db.hkeys(self.name())

	def all(self):
		'''
		获取所有键值对
		'''
		return self.db.hgetall(self.name())


if __name__ == '__main__':
	conn = RedisClient('accounts', 'weibo')
	result = conn.set('hello', 'sss')
	print(result)











































