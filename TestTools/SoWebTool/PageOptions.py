from selenium import webdriver
from selenium.webdriver.common.by import By
from basepage import SogaaPage

class WebElements(SogaaPage):

	username_loc = (By.ID, 'login_username')
	password_loc = (By.ID, 'login_password')
	button_loc = (By.XPATH, '//*[@id="loginForm"]/button')

	cx_loc = (By.XPATH, '/html/body/div[1]/header/nav/ul/li/global-search/div/div/button')					#查询
	# sq_loc = (By.XPATH, '')				#询价
	so_loc = (By.XPATH, '/html/body/div[1]/header/nav/ul/li/global-search/div/div/ul/li[2]/a')				#订单
	sp_loc = (By.XPATH, '/html/body/div[1]/header/nav/ul/li/global-search/div/div/ul/li[3]/a')				#采购
	ck_loc = (By.XPATH, '/html/body/div[1]/header/nav/ul/li/global-search/div/div/ul/li[4]/a')				#仓库
	user_loc = (By.XPATH, '/html/body/div[1]/header/nav/ul/li/global-search/div/div/ul/li[7]/a')			#客户
	supplier_loc = (By.XPATH, '/html/body/div[1]/header/nav/ul/li/global-search/div/div/ul/li[8]/a')		#供应商
	number_loc = (By.XPATH, '/html/body/div[1]/header/nav/ul/li/global-search/div/input')					#搜索框
	search_loc = (By.XPATH, '/html/body/div[1]/header/nav/ul/li/global-search/div/span/button')				#查询按钮

	def open(self):
		self._open(self.base_url)


	def  input_username(self, username):
		self.find_element(*self.username_loc).send_keys(username)

	def  input_password(self, password):
		self.find_element(*self.password_loc).send_keys(password)

	def input_number(self, args):
		self.find_element(*self.number_loc).send_keys(args)

	def click_submit(self):
		self.find_element(*self.button_loc).click()

	# def click_element_sq(self):
	# 	self.find_element(*self.cx_loc).click()
	# 	self.find_element(*self.sq_loc).click()

	def click_element_so(self):
		self.find_element(*self.cx_loc).click()
		self.find_element(*self.so_loc).click()

	def click_element_sp(self):
		self.find_element(*self.cx_loc).click()
		self.find_element(*self.sp_loc).click()

	def click_element_ck(self):
		self.find_element(*self.cx_loc).click()
		self.find_element(*self.ck_loc).click()

	def click_element_user(self):
		self.find_element(*self.cx_loc).click()
		self.find_element(*self.user_loc).click()

	def click_element_supplier(self):
		self.find_element(*self.cx_loc).click()
		self.find_element(*self.supplier_loc).click()

	def click_search(self):
		self.find_element(*self.search_loc).click()

class WebOptions(object):

	def __init__(self):
		self.driver = webdriver.Chrome()
		self.driver.implicitly_wait(20)
		self.url = 'http://www.sogaa.net/work/page/login'
		self.username = 'zlzhou@sogaa.net'
		self.password = 'sujia123456'
		self.page = WebElements(self.driver, self.url)

	def login(self):
		self.page.open()
		self.page.input_username(self.username)
		self.page.input_password(self.password)
		self.page.click_submit()


	def search_sq(self, *args):
		
		# search_page.click_element_sq(sq_number)
		self.page.input_number(args)
		self.page.click_search()

	def search_so(self, *args):
		self.page.click_element_so()
		self.page.input_number(args)
		self.page.click_search()

	def search_sp(self, *args):
		self.page.click_element_sp()
		self.page.input_number(args)
		self.page.click_search()

	def search_ck(self, *args):
		self.page.click_element_ck()
		self.page.input_number(args)
		self.page.click_search()

	def search_user(self, *args):
		self.page.click_element_user()
		self.page.input_number(args)
		self.page.click_search()

	def search_supplier(self, *args):
		self.page.click_element_supplier()
		self.page.input_number(args)
		self.page.click_search()

if __name__ == '__main__':
	SoLogin = WebOptions()
	SoLogin.login()
	# SoLogin.search_sq()		#查询价
	# SoLogin.search_so()		#查订单
	# SoLogin.search_sp()		#查采购
	# SoLogin.search_ck()		#查仓库
	# SoLogin.search_user()		#查客户
	SoLogin.search_supplier()	#查供应商