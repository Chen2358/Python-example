#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SogaaPage(object):

	def __init__(self, selenium_driver, base_url):
		self.base_url = base_url
		self.driver = selenium_driver

	def _open(self, url):
		self.driver.get(url)
		self.driver.maximize_window()

	def open(self):
		self._open(self.base_url)

	#重写元素定位
	def find_element(self, *loc):
		try:
			WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(loc))	#确保元素可见
			return self.driver.find_element(*loc)

		except AttributeError:
			print(f"%s 页面中未找到 %s 元素" % (self, loc))


	#重写send_keys		
	def send_keys(self, loc, value, clear_first=True, click_first=True):
		try:
			loc = getattr(self, "_%s" % loc)
			if click_first:
				self.loc.click()
			if clear_first:
				self.loc.clear()
				self.loc.send_keys(value)
		except AttributeError:
			print(f"%s 页面中未找到 %s 元素" % (self, loc))