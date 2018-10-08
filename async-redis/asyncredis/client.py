#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class Client(object):
	def __init__(self, host="localhost", port=6379, password=None, db=None, io_loop=None):
		self._io_loop = io_loop or IOLoop.current()
		self.connection = Connection(host=host, port=port, io_loop=self._io_loop)
		self.password = password
		self.db = db or 0
		#TODO
	
	#格式化命令
	def format_command(self, *tokens, **kwargs):
		cmds = []
		for t in tokens:
			e_t = self.encode(t)
			e_t_s = to_basestring(e_t)
			cmds.append("$%s\r\n%s\r\n" % (len(e_t), e_t_s))
		return "*%s\r\n%s" % (len(tokens), "".join(cmds))

	#格式化返回数据
	def format_reply(self, cmd_line, data):
		cmd = cmd_line.cmd
		#
		if cmd == "AUTH":
			return bool(data)
		#
		elif cmd == "SELECT":
			return data == "OK"
		#
		elif cmd == "SET":
			return data == "OK"
		else:
			return data

	#执行命令
	@gen.coroutine
	def execute_command(self, cmd, *args, **kwargs):
		result = None
		com_line =CmdLine(cmd, *args, **kwargs)
		#尝试2次
		n_tries = 2
		while n_tries > 0:
			n_tries -= 1
			if not self.connection.connected():
				self.connection.connect()

			if cmd not in ("AUT", "SELECT"):
				#进行认证
				if self.password and self.connection.info.get("pass", None) != self.password:
					yield self.auth(self.password)
				#选择数据库
				if self.db and self.connection.info.get("db", 0) != self.db:
					yield self.select(self.db)
			#格式命令
			command = self.format_command(cmd, *args, **kwargs)
			try:
				#发送数据
				yield self.connection.write(command)
			except Exception as e:
				self.connection.disconnect()
				if not n_tries:
					raise e
				else:
					continue

			#读取数据
			data = yield self.connection.read_line()
			if not data:
				if not n_tries:
					raise ConnectionError("not data received!!")
			else:
				resp = self.process_data(data, cmd_line)
				if isinstance(resp, partial):
					resp = yield resp()
				result = self.format_reply(cmd_line, resp)
				break

		#
		return result

	#处理 bulk 数据
	@gen.coroutine
	def _consume_bulk(self, tail):
		response = yield self.connection.read(int(tail) + 2)
		if isinstance(response, Exception):
			raise response
		if not response:
			raise ResponseError("empty response!")
		else:
			response = to_unicode(response)
			response = response[:-2]
		return response

	#根据Redis协议判断是否含有后续数据进行处理
	def process_data(self, data, cmd_line):
		data = to_basestring(data)
		data = data[:-2]		# strip \r\n

		if data == '$-1':
			response = None
		elif data == '*0' or data == '*-1':
			response = []
		else:
			head, tail = data[0], data[1:]

			if head == '*':
				return partial(self.consume_multibule, int(tail), cmd_line)
			elif head == '$':
				return partial(self._consume_bulk,tail)
			elif head == '+':
				response= tail
			elif head = ':':
				response = int(tail)
			elif head == '-':
				if tail.startswith('ERR'):
					tail = tail[4:]
				response = ResponseError(tail, cmd_line)
			else:
				raise ResponseError('unknown response type %s.' % head, cmd_line)
		return response

		#TODO

		#设置Key
		@gen.coroutine
		def set(self, key, value):
			result = yield self.execute_command("SET", key, value)
			return result
		#获取key
		@gen.coroutine
		def get(self, key):
			value = yield self.execute_command('GET', key)
			return value







