#-*- coding: utf-8 -*-

from hashlib import md5
import requests

class Chaojiying(object):

	def __init__(self, username, password, soft_id):
		self.username = username
		self.password = md5(password.encode('utf-8')).hexdigest()
		self.soft_id = soft_id
		self.base_params = {
			'user': self.username,
			'pass2': self.password,
			'softid': self.soft_id
		}

		self.headers = {
			'Connection': 'Keep-Alive',
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
		}

	#传入图片对象和验证码的代号
	def post_pic(self, im, codetype):
		'''
		im: 图片字符
		codetype: 题目类型，参考https://www.chaojiying.com/price.html
		'''
		params = {
			'codetype': codetype,
		}
		params.update(self.base_params)
		files = {'userfile': ('ccc.jpg', im)}
		r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, files=files, headers=self.headers)
		return r.json()

	#发生错误时回调
	def report_error(self, im_id):
		'''
		im_id:报错题目的图片ID
		'''
		params = {
			'id': im_id,
		}
		params.update(self.base_params)
		r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
		return r.json()