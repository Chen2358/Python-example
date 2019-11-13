#-*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import parse
import os



class Dispatcher:
	#自定义的具体时间处理程序被自动调用
	#负责查找合适的处理程序、创建参数元素并使用这些参数调用处理程序
	def dispatch(self, prefix, name, attrs=None):
		#根据前缀和标签名生成处理程序的名称
		mname = prefix + name.capitalize()
		#根据前缀生成默认处理程序名称
		dname = 'default' +prefix.capitalize()
		#尝试获取处理程序
		method = getattr(self, mname, None)
		#若可调用则将args设置为一个空元祖
		if callable(method): args = ()
		else:
			#否则尝试使用默认处理程序
			method = getattr(self, dname, None)
			#将args 设置为一个只包含标签名的元祖（默认处理程序只需要标签名）
			args = name,
		#如果调用的是起始程序，将属性添加到参数元祖（args）中
		if prefix == 'start': args += attrs,
		#如果获得的处理程序是可调用的，则使用正确的参数调用
		if callable(method): method(*args)

	def startElement(self, name, attrs):
		self.dispatch('start', name, attrs)

	def endElement(self, name):
		self.dispatch('end', name)

class WebsiteConstructor(Dispatcher, ContentHandler):

	passthrough = False

	#将根目录传递给构造函数
	def __init__(self, directory):
		self.directory = [directory]
		self.ensureDirectory()

	#确保当前目录已创建OK
	def ensureDirectory(self):
		path = os.path.join(*self.directory)
		# os.makedirs(path, exist_os=True)
		os.makedirs(path)

	def characters(self, chars):
		if self.passthrough: self.out.write(chars)

	#默认处理程序
	def defaultStart(self, name, attrs):
		if self.passthrough:
			self.out.write('<' + name)
			for key, val in attrs.items():
				self.out.write(' {}="{}"'.format(key, val))
			self.out.write('>')

	def defaultEnd(self, name):
		if self.passthrough:
			self.out.write('</{}>'.format(name))

	#支持目录
	def startDirectory(self, attrs):
		#当前目录路径存储在变量directory 包含的目录名列表中，
		#进入某个目录则将其名称附加到这个列表末尾
		self.directory.append(attrs['name'])
		self.ensureDirectory()

	#离开时将其名称从目录列表弹出
	def endDirectory(self):
		self.directory.pop()

	def startPage(self, attrs):
		filename = os.path.join(*self.directory + [attrs['name'] + '.html'])
		self.out = open(filename, 'w')
		self.writeHeader(attrs['title'])
		self.passthrough = True

	def endPage(self):
		self.passthrough = False
		self.writeFooter()
		self.out.close()

	#写入首部
	def writeHeader(self, title):
		self.out.write('<html>\n <head>\n    <title>')
		self.out.write(title)
		self.out.write('</title>\n </head>\n <body>\n')

	#写入尾部
	def writeFooter(self):
		self.out.write('\n </body>\n</html>\n')


parse('website.xml', WebsiteConstructor('public_html'))












































