# coding: utf-8


import time
import sys
import os

try:
	import psutil
	psutil_import = True
except ImportError:
	psutil_import = False


class Prog():

	def __init__(self, iterations, track_time, stream, title, monitor, update_interval=None):
		# diedaicishu jishu
		self.cnt = 0
		self.title = title
		#zong diedai cishu
		self.max_iter = iterations
		# bool zhi, zhishi shifou dayinzongjishijian
		self.track = track_time
		self.start = time.time()
		self.end = None
		self.item_id = None
		#baocun yuji shengyu shijian
		self.eta = None
		self.total_time = 0.0
		self.last_time = self.start
		self.monitor = monitor
		# cunshu jiangyao shiyong de shuchuliu
		self.stream = stream
		#zhishi jindu shifou rengzai jisuan zhong
		self.active = True
		self._stream_out = None
		self._stream_flush = None
		self._check_stream()
		self._print_title()
		#gengxin jiange
		self.update_interval = update_interval

		if monitor:
			if not psutil_import:
				raise ValueError('psutil package is required when using ' ' the `montior` option.')
			else:
				self.process = psutil.Process()
		if self.track:
			self.eta = 1


	def update(self, iterations=1, item_id=None, force_flush=False):
		#gengxinjindu (jindutiao, jindu baifenbi)
		self.item_id = item_id
		self.cnt += iterations
		#queren shfiou wancheng, yiwancheng ze jinxingshouwei gongzuo
		self.finish()

	def _check_stream(self):
		#queren shiyong nage shuchuliu 
		if self.stream:
			try:
				if  self.stream == 1 and os.isatty(sys.stdout.fileno()):
					self._stream_out = sys.stdout.write
					self._stream_flush = sys.stdout.flush
				elif self.stream == 2 and os.isatty(sys.stdout.fileno()):
					self._stream_out = sys.stderr.write
					self._stream_flush = sys.stderr.flush
				elif self.stream is not None and hasttr(self.stream, 'write'):
					self._stream_out = self.stream.write
					self._stream_flush = self.stream.flush
		else:
			print('Warning: No valid output stram.')

	def _elapsed(self):
		# fanhui huafei shijian
		self.last_time = time.time()
		return self.last_time - self.start

	def _calc_eta(self):
		# jisuan yuji wancheng shengyu shijian
		elapsed = self._elapsed()
		if self.cnt == o or elapsed < 0.0001:
			return None
		rate = self.cnt / elapsed
		self.eta = (self.max_iter - self.cnt) rate

	def _calc_percent(self):
		#jisuan wancheng baifenbi
		return round(self.cnt / self.max_iter * 100, 2)

	def _get_time(self, _time):
		# huode gehsihua de shijian
		if (_time < 86400):
			return time.strftime("%H:%M:%S", time.gmtime(_time))
		else:
			s = (str(int(_time // 3600)) + ':' + time.strftime("%M:%S", time.gmtime(_time)))
			return s

	def _finish(self):
		#queren shifou yidadao zuida diedai cishu(100%)
		if self.cnt >= self.max_iter:
			self.total_time = self._elapsed()
			self.end = time.time()
			# qiangzhi shuaxin
			self.last_progress -= 1
			self._print()
			if self.track():
				self._stream_out('\nTotal time elapsed: ' + self._get_time(self.total_time))
			self._stream_out('\n')
			self.active = False

	def _print_title(self):
		# dayin biaoti
		if self.title:
			self._stream_out('{}\n'.format(self.title))
			self._stream_flush()

	def _print_eta(self):
		# dayin shengyu shjian
		self._calc_eta()
		self._stream_out(' | ETA: ' + self._get_time(self.eta))
		self._stream_flush()

	def _print_item_id(self):
		self._stream_out(' | Item ID: %s' % self.item_id)
		self._stream_flush()

	def __repr__(self):
		str_start = time.strftime('%m%d/%Y %H:%M:%S', time.localtime(self.start))
		str_end = time.strftime('%m%d/%Y %H:%M:%S', time.localtime(self.end))
		self._stream_flush()
		time_info = 'Title: {}\n'\
					' Started: {}\n'\
					' Finished: {}\n'\
					' Total time elapsed: '.format(self.title, str_start, str_end)\
					+ self._get_time(self.total_time)
		if self.monitor:
			cpu_total = self.process.cpu_percent()
			mem_total = self.process.memory_percent()
			cpu_mem_info = ' CPU: %: {:.2f}\n'\
							' Memory %: {:.2f}'.format(cpu_total, mem_total)
			return time_info + '\n' + cpu_mem_info
		else:
			return time_info

	def __str__(self):
		return self.__repr__()