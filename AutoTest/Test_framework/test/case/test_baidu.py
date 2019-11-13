# -*-* coding: utf-8 -*-


import time
import unittest
from utils.config import Config, DATA_PATH, REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.mail import Email
from test.page.baidu_result_page import BaiDuMainPage, BaiDuResultPage
import sys



class TestBaiDu(unittest.TestCase):

	URL = Config().get('URL')
	excel = DATA_PATH + 'test.xlsx'


	def sup_setUp(self):
		self.page = BaiDuMainPage(browser_type='chrome').get(self.URL, maximize_window=False)

	def sub_tearDown(self):
		self.driver.quit()


	# def test_search_0(self):
	# 	self.driver.find_element(*self.locator_kw).send_keys('selenium')
	# 	self.driver.find_element(*self.locator_su).click()
	# 	time.sleep(2)

	# 	links = driver.find_elements(*self.locator_result)
	# 	for link in links:
	# 		print(link.text)

	# def test_search_1(self):
	# 	self.driver.find_element(*self.locator_kw).send_keys('Python selenium')
	# 	self.driver.find_element(*self.locator_su).click()
	# 	time.sleep(2)

	# 	links = driver.find_elements(*self.locator_result)
	# 	for link in links:
	# 		print(link.text)

	def test_search(self):
		datas = ExcelReader(self.excel).data
		for d in datas:
			with self.subTest(data=d):
				self.sub_setUP()
				self.page.search(d['search'])
				time.sleep(2)

				self.page = BaiDuResultPage(self.page)		#跳转到reult page

				links = self.page.result_links()
				for link in links:
					print(link.text)
				self.sub_tearDown()

if __name__ == '__main__':
	report = REPORT_PATH + '\\report.html'
	with open(report, 'wb') as f:
		runner = HTMLTestRunner(f, verbosity=2, title='testReport', description='测试报告')
		runner.run(TestBaiDu('test_search'))

	# e = Email(title='XXX测试报告',
	# 		  message='测试报告，请查收！',
	# 		  receiver='...',
	# 		  server='...',
	# 		  password='...',
	# 		  path=report
	# 		  )
	# e.send()



