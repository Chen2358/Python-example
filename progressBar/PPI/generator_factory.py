# coding: utf-8

from .progbar import ProgBar
from .progpercent import ProgPercent

def generator_factory(mother_class):
	def generator_progress(iteritem, iterations=None, *args, **kw):
		#形参列表中的*args 表示函数接收任意数量的参数并封装为元祖；**kw 表示函数接收任意数量的关键字参数并封装为字典 kw。
		if iterations is None:
			iterations = len(iteritem)
		mbar = mother_class(iterations, *args, **kw)
		#实参列表中的*args 和**kw 是解包操作，把元祖 args 解包为一个个参数，把字典kw 解包为一系列关键字参数	
		for item in iteritem:
			yield item
			mbar.update()
	return generator_progress

prog_percent = generator_factory(ProgPercent)
prog_bar = generator_factory(ProgBar)
