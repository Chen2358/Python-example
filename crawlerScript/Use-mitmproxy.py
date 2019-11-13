#-*- coding: utf-8 -*-

import json
imoprt pymongo
from mitmproxy import ctx

client = pymongo.MongoClient('localhost')
db = client('igetget')
collection = db['books']

def response(flow):
	global collection
	url = 'https://dedap.igetget.com/v3/discover/booklist'
	if flow.request.url.startswith(url):
		text = flow.response.text
		data = json.loads(text)
		books = data.get('c').get('list')
		for book in books:
			# ctx.log.info(str(book)) #控制台输出
			data = {
				'title': book.get('operating_title'),
				'cover': book.get('cover'),
				'summary': book.get('other_share_summary'),
				'price': book.get('price')
			}
			ctx.log.info(str(data))
			collection.insert(data)

			