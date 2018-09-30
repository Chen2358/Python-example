#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import asyncredis
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.gen
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('app')

class MainHandler(tornado.web.RequestHandler):

	@tornado.gen.coroutine
	def get(self):
		c = asyncredis.Client
		#
		shiyan = yield tornado.gen.Task(c.get, "shiyan")
		self.set_header("Content-Type", "text/html")
		self.render("template.html", title="Simple demo", shiyan=shiyan)

application = tornado.web.Application([
	(r'/', MainHandler),
])

#
@tornado.gen.coroutine
def create_test_data():
	c = asyncredis.Client()
	yield c.select(0)
	yield c.set("shiyan", "test")

if __name__ == '__main__':
	create_test_data()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	print("Demo is run at 0.0.0.0:8888")
	tornado.ioloop.IOLoop.instance().start()