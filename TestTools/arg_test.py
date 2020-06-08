#coding: utf-8

'''
#对位置参数的基本范围测试
def rangetest(*argschecks):
	def onDecorator(func):
		if not __debug__:			#默认为True，-O关闭
			return func
		else:
			def onCall(*args):
				for (ix, low, high) in argschecks:
					if args[ix] < low or args[ix] > high:
						errmsg = 'Argument %s not in %s..%s' % (ix, low, high)
						raise TypeError(errmsg)
				return func(*args)
			return onCall
	return onDecorator

@rangetest((1, 0, 120))
def persinfo(name, age):
	print('%s is %s years old' % (name, age))

@rangetest([0, 1, 12], [1, 1, 31], [2, 0, 2009])
def  birthday(M, D, Y):
	print('birthday = {0}/{1}/{2}'.format(M, D, Y))

class Person:

	def __init__(self, name, job, pay):
		self.job = job
		self.pay = pay

	@rangetest([1, 0.0, 1.0])
	def giveRaise(self, percent):
		self.pay = int(self.pay * (1 + percent))


if __name__ == '__main__':
	print(__debug__)		#True

	persinfo('Bob', 45)

	birthday(5, 31, 1963)

	sue = Person('sue', 'dev', 100000)
	sue.giveRaise(.10)
	print(sue.pay)

	# sue.giveRaise(1.10)		#typeerror
'''

#对关键字和默认泛化

trace = True

def rangetest(**argschecks):
	def onDecorator(func):
		if not __debug__:			#默认为True，-O关闭
			return func
		else:
			import sys
			code = func.__code__
			allargs = code.co_varnames[:code.co_argcount]		#.__code__.co_varnames:返回参数元组
			funcname = func.__name__

			def onCall(*pargs, **kargs):
				positionals = list(allargs)
				positionals = positionals[:len(pargs)]

				for (argname, (low, high)) in argschecks.items():
					if argname in kargs:
						if kargs[argname] < low or kargs[argname] > high:
							errmsg = '{0} argument "{1}" not in {2}...{3}'
							errmsg = errmsg.format(funcname, argname, low, high)
							raise TypeError(errmsg)
					elif argname in positionals:
						position = positionals.index(argname)
						if pargs[position] < low or pargs[position] > high:
							errmsg = '{0} argument "{1}" not in {2}...{3}'
							errmsg = errmsg.format(funcname, argname, low, high)
							raise TypeError(errmsg)
					else:
						if trace:
							print('Argument "{0}" defaulted'.format(argname))
					return func(*pargs, **kargs)
			return onCall
	return onDecorator

@rangetest(age=(0, 120))
def persinfo(name, age):
	print('%s is %s years old' % (name, age))

@rangetest(M=(1, 12), D=(1, 31), Y=(0, 2009))
def  birthday(M, D, Y):
	print('birthday = {0}/{1}/{2}'.format(M, D, Y))

class Person:

	def __init__(self, name, job, pay):
		self.job = job
		self.pay = pay

	@rangetest(percent=(0.0, 1.0))
	def giveRaise(self, percent):
		self.pay = int(self.pay * (1 + percent))

@rangetest(a=(1, 10), b=(1, 10), c=(1, 10))
def omitargs(a, b=7, c=8):
	print(a, b, c)
	
if __name__ == '__main__':
	persinfo('Bob', 40)
	persinfo(age=40, name='Bob')
	# persinfo(age=140, name='Bob')		#error
	birthday(5, D=1, Y=1965)
	birthday(5, D=40, Y=1963)
	sue = Person('sue', 'dev', 100000)
	sue.giveRaise(percent=.20)
	print(sue.pay)
	# sue.giveRaise(percent=1.20)			#error

	omitargs(1, 2, 3)
	omitargs(1, 2, 11)



