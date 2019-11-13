#-*- coding: utf-8 -*-

from nntplib import NNTP, decode_header
from urllib.request import urlopen
import textwrap
import re


class NewsAgent:
	"""
	可将新闻源中的新闻分发到新闻目的地的对象
	"""
	def __init__(self):
		self.sources = []
		self.destinations = []

	#添加源
	def add_source(self, source):
		self.sources.append(source)

	#添加目的地
	def addDestination(self, dest):
		self.destinations.append(dest)

	#遍历所有新闻源，并创建一个新闻列表；
	#并遍历所有目的地，并将完整的新闻列表提供给每个目的地
	def distribute(self):
		"""
		从所有新闻源获取所有的新闻，并将其分发到所有新闻目的地
		"""
		items = []
		for source in self.sources:
			items.extend(source.get_items())
		for dest in self.destinations:
			dest.receive_items(items)


class NewsItem:
	"""
	由标题和正文组成的简单新闻
	"""
	def __init__(self, title, body):
		self.title = title
		self.body = body


class NNTPSource:
	"""
	从NNTP新闻组获取新闻的新闻源
	"""
	def __init__(self, servername, group, howmany):
		self.servername = servername
		self.group = group
		self.howmany = howmany

	def get_items(self):
		server = NNTP(self.servername)
		#服务器响应、新闻组包含的消息数、第一条和最后一条消息编号、新闻组名称
		resp, count, first, last, name = server.group(self.group)
		#确定要获取的文章编号区间的起始位置 
		start = last - self.howmany + 1
		resp, overviews = server.over((start, last))
		for id, over in overviews:
			title = decode_header(over['subject'])
			resp, info = server.body(id)
			body = '\n'.join(line.decode('latin') for line in info.lines) + '\n\n'
			yield NewsItem(title,  body)
		server.quit()


class SimpleWebSource:
	"""
	从网页提取新闻的新闻源
	"""
	def __init__(self, url, title_pattern, body_pattern, encoding='utf-8'):
		self.url = url
		self.title_pattern = re.compile(title_pattern)
		self.body_pattern = re.compile(body_pattern)
		self.encoding = encoding

	def get_items(self):
		text = urlopen(self.url).read().decode(self.encoding)
		titles = self.title_pattern.findall(text)
		bodies = self.body_pattern.findall(text)
		for title, body in zip(titles, bodies):
			yield NewsItem(title, textwrap.fill(body) + '\n')


class PlainDestination:
	"""
	以纯文本方式显示所有新闻的新闻目的地
	"""
	def receive_items(self, items):
		for item in items:
			print(item.title)
			print('-' * len(item.title))
			print(item.body)

class HTMLDestination:
	"""
	以HTML显示所有新闻的新闻目的地
	"""
	def __init__(self, filename):
		self.filename = filename

	def receive_items(self, items):
		out = open(self.filename, 'w')
		print("""
			<html>
				<head>
					<title>Today's News</title>
				</head>
				<body>
				<h1>Today's News</h1>
			""", file=out)
		print('<ul>', file=out)
		id = 0
		for item in items:
			id += 1
			print('<h2><a name="{}">{}</a></h2>'.format(id, item.title),file=out)
		print("""
				</body>
			</html>
			""", file=out)

def runDefaultSetup():
	"""
	设置新闻源和目的地
	"""
	agent = NewsAgent()

	#从网页获取新闻的SimpleWebSource对象
	reuters_url = 'http://news.baidu.com/'
	reuters_title = r'<strong><a href="([a-zA-z]+://[^\s]*)></a>/strong>'
	reuters_body = r'test'
	reuters = SimpleWebSource(reuters_url, reuters_title, reuters_body)

	agent.add_source(reuters)

	'''
	#从comp.lang.python.announce获取新闻的NNTPSource对象
	clpa_server = 'news.foo.bar'		
	#服务器
	clpa_server = 'news.ntnu.no'
	#设置指定的新闻组为当前新闻组
	clpa_group = 'comp.lang.python.announce'
	#获取新闻数
	clpa_howmany = 10
	clpa = NNTPSource(clpa_server, clpa_group, clpa_howmany)
	agent.add_source(clpa)
	'''
	#添加纯文本和HTML目的地
	agent.addDestination(PlainDestination())
	agent.addDestination(HTMLDestination('news.html'))

	#
	agent.distribute()

if __name__ == '__main__':
	runDefaultSetup()






































