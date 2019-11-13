# -*-* coding: utf-8 -*-

import time
from selenium.webdriver.common.action_chains import AcitonChains
from test.common.browser import Browser
from utils.log import logger


class Page(Browser):

	def __init__(self, page=None, browser_type='chorme'):
		if page:
			self.driver = page.driver
		else:
			super(Page, self).__init__(browser_type=browser_type)

	@property
	def current_window(self):
		return self.dirver.current_window_handle

	@property
	def title(self):
		return self.driver.title

	@property
	def current_url(self):
		return self.driver.current_url

	def get_driver(self):
		return  self.driver

	def wait(self, seconds=3):
		time.sleep(seconds)

	def execute(self, js, *args):
		self.driver.execute_script(js, *args)

	def move_to(self. element):
		AcitonChains(self.dirver).move_to_element(element).perform()

	def find_element(self, *args):
		return self.driver.find_element(*args)

	def find_elements(self, *args):
		return self.driver.find_elements(*args)

	def switch_to_window(self, partial_url='', partial_title=''):
		"""如果窗口数<3，不需传入参数，切换到当前窗口外的窗口；
			窗口数>3，需要传入参数确定跳转到哪个窗口"""
		all_windows = self.driver.window_handles
		if len(all_windows) == 1:
			logger.warning('只有一个窗口！')
		elif len(all_windows) == 2:
			other_window = all_windows[1 - all_windows.index(self.current_window)]
			self.driver.switch_to_window(other_window)
		else:
			for window in all_windows:
				self.driver.switch_to_window(window)
				if partial_url in self.driver.current_url or partial_title in self.driver.title:
					break
		logger.debug(self.driver.current_url, self.driver.title)

		def switch_to_frame(self, param):
			sel.driver.switch_to_frame(param)

		def switch_to_alert(self):
			return self.driver.switchto.alert


















