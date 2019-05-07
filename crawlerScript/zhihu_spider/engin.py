# -*- coding: utf-8 -*-

import sys
from imp import reload
reload(sys)


import gevent
import redis
import crawler
import time
from multiprocessing.dummy import Pool
import multiprocessing


red_queue="test_the_url_queue"
red_crawled_set="test_url_has_crawled"

process_pool=Pool(multiprocessing.cpu_count()*2)



#connect to redis server
red=redis.Redis(host='localhost', port=6379, db=1)


def re_crawl_url(url):
	red.lpush(red_queue,url)

def check_url(url):
	if red.sadd(red_crawled_set,url):
		red.lpush(red_queue,url)

#wrap the class method
def create_new_slave(url,option):
	new_slave=crawler.Zhihu_Crawler(url,option)
	new_slave.send_request()
	return "ok"

def gevent_worker(option):
	while True:
		url=red.lpop(red_queue)
		if not url:
			break
		create_new_slave(url,option)

def process_worker(option):
	jobs=[]
	for i in range(50):
		jobs.append(gevent.spawn(gevent_worker,option))
	gevent.joinall()



if __name__=="__main__":

	'''
	start the crawler

	'''

	start=time.time()
	count=0

	#choose the running way of using database or not

	try:
		option=sys.argv[1]
	except:
		option=''
	if "mongo" not in option:
		option="print_data_out"

	#the start page

	red.lpush(red_queue,"https://www.zhihu.com/people/gaoming623")
	url=red.lpop(red_queue)
	create_new_slave(url,option=option)
	for i in range(50):
		gevent_worker(option=option)

	process_pool.map_async(process_worker,option)
	process_pool.close()
	process_pool.join()


	print("crawler has crawled %d people ,it cost %s" % (count,time.time()-start))



















