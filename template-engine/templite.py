#!/usr/bin/env python3

import re

class TempliteSyntaxError(ValueError):
	pass


#代码构建器
class CodeBuilder(object):
	def __init__(self, indent=0):
		self.code = []
		self.indent_level = indent

	#返回生成的代码字符串
	def __str__(self):
		return "".join(str(c) for c in self.code)

	#添加代码	
	def add_line(self, line):
		self.code.extend([" " * self.indent_level, line, "\n"])		#自动缩进

	#添加占位
	def add_section(self):
		section = CodeBuilder(self.indent_level)
		self.code.append(section)
		return section

	#增长和缩进
	INDENT_STEP = 4
	
	def indent(self):
		self.indent_level += self.INDENT_STEP

	def dedent(self):
		self.indent_level -= self.INDENT_STEP

	#返回代码运行结果
	def get_globals(self):
		#检查缩进
		assert self.indent_level == 0
		#得到生成的代码
		python_source = str(self)
		# 运行代码后得到的名字空间（变量字典）
		global_namespace = {}
		#如果没有local_namespace参数，则global_namespace会同时包含局部与全局的变量
		exec(python_source, global_namespace)
		return global_namespace


#编译和渲染
class Templite(object):

	def __init__(self, text, *contexts):

		"""`text`是输入的模板

        `contexts`是输入的数据与过滤器函数

        """
		self.context = {}
		for context in contexts:
			self.context.update(context)

		#所有的变量名
		self.all_vars = set()
		#属于循环的变量名
		self.loop_vars = set()

		#开始添加代码
		code = CodeBuilder()

		code.add_line("def render_function(context, do_dots):")
		code.indent()
		#先加个section占位，从上下文提取变量的代码在之后实现
		vars_code = code.add_section()
		code.add_line("result = []")
		code.add_line("append_result = result.append")
		code.add_line("extend_result = result.append")
		code.add_line("to_str = str")
		
		buffered = []
		def flush_output():
			#如果追加的代码段只有一个使用append
			if len(buffered) == 1:
				code.add_line("append_result(%s)" % buffered[0])
			#如果追加的代码段只有一个使用append
			elif len(buffered) > 1:
				code.add_line("extend_result([%s])" % ", ".join(buffered))
			#清空缓存
			del buffered[:]

		#检查嵌套是否正确
		ops_stack = []

		tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)

		for token in tokens:
			#注释
			if token.startswith('{#'):
				continue
			#替换
			elif token.startswith('{{'):
				# 得到Python表达式
				expr = self._expr_code(token[2:-2].strip())
				buffered.append("to_str(%s)" % expr)
			#控制结构
			elif token.startswith('{%'):

				flush_output()
				words = token[2:-2].strip().split()
				#if标签
				if words[0] == 'if':
					if len(words) != 2:
						self._syntax_error("Don't understand if", token)
					ops_stack.appen('if')
					code.add_line("if %s:" % self._expr_code(words[1]))
					code.indent()
				#for标签
				elif words[0] == 'for':
					if len(words) != 4 or words[2] != 'in':
						self._syntax_error("Don't understand for", token)
					ops_stack.append('for')
					self._variable(words[1], self.loop_vars)
					code.add_line(
						"for c_%s in %s:" % (
							words[1],
							self._expr_code(words[3])
						)
					)
					code.indent()
				# end 标签
				elif words[0].startswith('end'):
					if len(words) != 1:
						self._syntax_error("Don't understand end", token)
					end_what = words[0][3:]
					if not ops_stack:
						self._syntax_error("Too many ends", token)
					start_what = ops_stack.pop()
					if start_what != end_what:
						self._syntax_error("Mismatched end tag", end_what)
					code.dedent()
				else:
					self._syntax_error("Don't understand tag", words[0])
			#处理文本
			else:
				if token:
					buffered.append(repr(token))

		if ops_stack:
			self._syntax_error("Unmatched action tag", ops_stack[-1])

		flush_output()

		for var_name in self.all_vars - self.loop_vars:
			vars_code.add_line("c_%s = context[%r]" % (var_name, var_name))

		code.add_line("return ''.join(result)")
		code.dedent()
		self._render_function = code.get_globals()['render_function']

	def _expr_code(self, expr):
		if "|" in expr:
			pipes = expr.split("|")
			code = self._expr_code(pipes[0])
			for func in pipes[1:]:
				self._variable(func, self.all_vars)
				code = "c_%s(%s)" % (func, code)

		elif "." in expr:
			dots = expr.split(".")
			code = self._expr_code(dots[0])
			args = ", ".join(repr(d) for d in dots[1:])
			code = "do_dots(%s, %s)" % (code, args)
	
		else:
			self._variable(expr, self.all_vars)
			code = "c_%s" % expr
		return code

	def _syntax_error(self, msg, thing):
		raise TempliteSyntaxError("%s: %r" % (msg, thing))

	def _variable(self, name, vars_set):
		if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
			self._syntaxerror("Not a valid name", name)
		vars_set.add(name)

	#渲染
	def render(self, context=None):
		render_context = dict(self.context)
		if context:
			render_context.update(context)
		return self._render_function(render_context, self._do_dots)

	def _do_dots(self, value, *dots):
		for dot in dots:
			try:
				value = getattr(value, dot)
			except AttributeError:
				value = value[dot]
			if callable(value):
				value = value()
		return value

