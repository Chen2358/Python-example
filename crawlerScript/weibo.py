#-*- coding: utf-8 -*-


#Ajax请求
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
	'Host': 'm.weibo.cn',
	'Refer': 'https://m.weibo.cn/u/2830678474',
	'User-Agent': "Mozila/5.0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36",
	'X-Requested-With': 'XMLHtppRequest',
}

def get_page(page):
	params = {
		'type': 'uid',
		'value': '2830678474',
		'containerid': '1076032830678474',
		'page': page
	}

	url = base_url + urlencode(params)
	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.json()
	except requests.ConnectionError as e:
		print('Error', e.args)


def parse_page(json):
	if json:
		items = json.get('data').get('cards')
		for item in items[2:]:		#返回的列表中的第二个不是微博内容
			item = item.get('mblog')
			weibo = {}
			weibo['id'] = item.get('id')
			weibo['text'] = pq(item.get('text')).text()
			weibo['attitudes'] = item.get('attitudes_count')
			weibo['comments'] = item.get('comments_count')
			weibo['reposts'] = item.get('reposts_count')
			yield weibo

if __name__ == '__main__':
	for page in range(1, 11):
		json = get_page(page)
		results = parse_page(json)
		for result in results:
			print(result)