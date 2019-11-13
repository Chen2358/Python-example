# -*- coding: utf-8 -*-
#https://cuiqingcai.com/3256.html


import requests
from bs4 import BeautifulSoup
import os

from Download import request

class mzitu(object):

	def __init__(self):
		self.headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

	def all_url(self, url):
		html = request.get(url, 3)
		# html = Download.get(self, url 3)
		all_a =  BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
		all_a.pop(0)
		for a  in all_a:
			title = a.get_text()
			print(u'开始保存: ', title)
			path = str(title),replace("?", '_')
			self.mkdirs(path)
			href = a['href']
			self.html(href)

	def html(self, href):
		html = request.get(href, 3)
		# html = Download.get(self,  href, 3)
		self.headers['referer'] = href
		max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
		for page in range(1, int(max_span)+1):
			page_url =  href + '/' + str(page)
			self.img(page_url)

	def img(self, page_url):
		img_html = request.get(page_url, 3)
		# img_url = Download.get(self, page_url, 3)	
		img_url = BeautifulSoup(img_html.text, 'lxml').find('div',class_='main-image').find('img')['src']
		self.save(img_url)

	def save(self, img_url):
		name = img_url[-9:-4]
		img = request.get(img_url, 3)
		# img = Download.get(self, img_url, 3)
		f = open(name+'.jpg', 'ab')
		f.write(img.content)
		f.close()

	def mkdir(self, path):
		path = path.strip()
		isExists = os.path.exists(os.path.join('E:\\mzitu', path))
		if not isExists:
			print(u'建了一个名字叫做', path, u'的文件！')
			os.makedirs(os.path.join('E:\\mzitu', path))
			os.chdir(os.path.join('E:\\mzitu', path))
			return True
		else:
			print(u'名为', path, u'的文件已存在！')
			return False

	def request(self, url):
		content = requests.get(url, headers=self.headers)
		return content

Mzitu = mzitu()
Mzitu.all_url('https://www.mzitu.com/tag/youhuo/')




































































