#-*- coding: utf-8 -*-



from selenium import webdriver
from selenium.webdriver.common.by import By
from BasePage import SogaaPage

class LoginPage(SogaaPage):

	username_loc = (By.ID, 'login_username')
	password_loc = (By.ID, 'login_password')
	button_loc = (By.XPATH, '//*[@id="loginForm"]/button')

	def open(self):
		self._open(self.base_url)


	def  input_username(self, username):
		self.find_element(*self.username_loc).send_keys(username)

	def  input_password(self, password):
		self.find_element(*self.password_loc).send_keys(password)

	def click_submit(self):
		self.find_element(*self.button_loc).click()












