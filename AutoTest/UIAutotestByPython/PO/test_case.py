#-*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.by import By
from webium import BasePage, Find, Finds
from LoginPage import LoginPage
import unittest



class CaseLoginWork(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.implicitly_wait(3)
		self.url = 'http://192.168.1.10:8080/work/page/login'
		self.username = 'sujia100@sogaa.net'
		self.password = '123456'

	def test_login(self):
		login_page = LoginPage(self.driver,self.url)
		login_page.open()
		login_page.input_username(self.username)
		login_page.input_password(self.password)
		login_page.click_submit()

	def tearDown(self):
		self.driver.quit()

if __name__ == '__main__':
	unittest.main()











