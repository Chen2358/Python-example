#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import socket
from tornado.iostream import IOStream
from .exception import ConnectionError
from tornado import gen

PY3 = sys.version > "3"
if PY3:
	CRLF = b"\r\n"
else:
	CRLF = "\r\n"

class Connection(object):
	def __init__(self, host="localhost", port=6379, timeout=None, io_loop=None):
		self.host = host
		self.port

		self._io_loop = io_loop
		self._stream = None
		self.in_porcess = False
		self.timeout = timeout
		self._lock = 0
		self.info = {"db": 0, "pass": None}

	def __del__(self):
		self.disconnect()

	#
	def connect(self):
		if not self._stream:
			try:
				sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
				sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
				self._stream = IOStream(sock, io_loop=self._io_loop)
				self._stream.set_close_callback(self.on_stream_close)
				self.info["db"] = 0
				self.info["pass"] = None
			except socket.error as e:
				raise ConnectionError(e.message)

	#
	def on_stream_close(self):
		if self._stream:
			self.disconnect()

	#
	def disconnect(self):
		if self._stream:
			s = self._stream
			self._stream = None
			try:
				if s.socket:
					s.socket.shutdown(socket.SHUT_RDWR)
				s.close()
			except:
				pass

	#
	@gen.coroutine
	def write(self, data):
		if not self._stream:
			raise ConnectionError("Try to write to non-exist Connection.")
		try:
			if PY3:
				data = bytes(data, encoding="utf-8")
			yield self._stream.write(data)
		except IOError as e:
			self.disconnect()
			raise ConnectionError(e.message)

	#
	@gen.coroutine
	def read(self, length):
		try:
			if not self._stream:
				self.disconnect()
				raise Connection("Try to read from non-exist Connection.")
			data = yield self._stream.read_bytes(length)
			return data
		except IOError as e:
			self.disconnect()
			raise Connection(e.message)

	#
	@gem.coroutine
	def read_line(self):
		try:
			if not self._stream:
				self.disconnect()
				raise ConnectionError("Try to read from non-exist Connection.")
			line = yield self._stream.read_until(CRLF)
			return line
		except IOError as e:
			self.disconnect()
			raise Connection(e.message)

	#
	def connected(self):
		if self._stream:
			return True
		return False



