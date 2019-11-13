# coding: utf-8


from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.by import By
from .base import Page
from time import sleep

class login(Page):

	'''
	登录页面
	'''

	url = '/portal/login'


	login_username_loc = (By.ID, "login_username")
	login_password_loc = (By.ID, "login_password")
	login_button_loc = (By.XPATH, "/html/body/div[8]/div/div/div/div[3]/div[1]/button")

	def login_username(self, username):
		self.find_element(*self.login_username_loc).send_keys(username)

	def login_password(self, password):
		self.find_element(*self.login_password_loc).send_keys(password)

	def login_button(self):
		self.find_element(*self.login_button_loc).click()


	#统一登录入口
	def user_login(self, username="cjcha3o@sogaa.net", password="123456"):
		'''
		获取用户名密码登录
		'''
		self.open()
		# self.bbs_login()
		self.login_username(username)
		self.login_password(password)
		self.login_button()

		sleep(3)

	user_error_hint_loc = (By.XPATH, '//*[@id="loginForm"]/div[2]/div[1]/div')
	# pawd_error_hint_loc = (By.XPATH, "")
	user_login_success_loc = (By.XPATH, "/html/body/div/header/nav/div[2]/ul[4]/li[3]/a/span")

	#用户名错误提示
	def user_error_hint(self):
		return self.find_element(*self.user_error_hint_loc).text

	#密码错误提示
	def pawd_error_hint(self):
		return self.find_element(*self.pawd_error_hint_loc).text

	#成功登录的用户名
	def user_login_success(self):
		return self.find_element(*self.user_login_success_loc).text












































































