# coding: utf-8

from pyprind.prog_class import Prog
import time

class ProgPercent(Prog):

	def __init__(self, iterations, track_time=True,
				stream=2,  title='', monitor=False, update_interval=None):
		Prog.__init__(self, iterations, track_time, stream, title, monitor, update_interval)

		# 保存上一进度百分比
		self.last_progress = 0
		self._print()
		if monitor:
			try:
				self.process.cpu_percent()
				self.process.memory_percent()
			except AttributeError:
				self.process.get_cpu_percent()
				self.process.get_memory_percent()

	def _print(self, force_flush=False):
		next_perc = self._calc_percent()
		if self.update_interval:
			do_update = time.time() - self.last_time >= self.update_interval
		elif force_flush:
			do_update = True
		else:
			do_update = next_perc > self.last_progress

		if do_update and self.active:
			self.last_progress = next_perc
			self._stream_out('\r[%3d %%]' % (self.last_progress))
			if self.track:
				self._stream_out(' Time elasped: ' + self._get_time(self._elapsed()))
				self._print_eta()
			if self.item_id:
				self._print_itme_id()
