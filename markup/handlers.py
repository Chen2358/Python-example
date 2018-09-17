#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
给文本块加上HTML标记
'''

class Handler:
	#处理程序父类
	
	def callback(self, prefix, name, *args):
		#返回一个对象的属性值
		method = getattr(self, prefix + name, None)
		#判断函数是否可被调用
		if callable(method): return method(*args)

	def start(self, name):
		self.callback('start_', name)

	def end(self, name):
		self.callback('end_', name)

	def sub(self, name):
		def substitution(match):
			result = self.callback('sub_', name, match)
			if result is None: result = match.group(0)
			return result
		return substitution

class HTMLRenderer(Handler):

	#HTML 处理程序，给文本块加对应的HTML标记
	def start_document(self):
		print('<html><head><title>Hello world</title></head><body>')

	def end_document(self):
		print('</body></html>')

	def start_paragraph(self):
		print('<p style="color: #444;">')

	def end_paragraph(self):
		print('/p')

	def start_heading(self):
		print('<h2 style="color: #68BE5D;">')

	def end_heading(self):
		print('</h2>')

	def start_list(self):
		print('<ul style="color: #363736;">')

	def end_list(self):
		print('</ul>')

	def start_listitem(self):
		print('<li>')

	def  end_listitem(self):
		print('</li>')

	def start_title(self):
		print('<h1 style="coclor: 1ABC9C;">')

	def end_title(self):
		print('</h1>')

	def sub_emphasis(self, match):
		return ('<a target="_blank" style="text-decoration: none;color: #BC1A4B;" href="%s">%s</a>' % 
			(match.group(1), match.group(1)))

	def sub_mail(self, match):
		return ('<a style="text-decoration: none;color: #BC1A4B;" href="mail to: %s">%s</a>' % 
			(match.group(1), match.group(1)))

	def feed(self, data):
		print(data)
