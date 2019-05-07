# -*- coding: utf-8 -*-

import redis

red_queue = "test_the_url_queue"
red_crawled_set = 'test_url_has_crawled'


process_pool = (multiprocessing.cpu_count() * 2)

#connect to redis server
red = redis.Redis(host='localhost', port=6379, db=1)

def re_crawl_url(url):
	red.lpush(red_queue, url)

def check_url(url):
	if red_sadd(red_crawled_set, url):
		red.lpush(red_queue, url)















