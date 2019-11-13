# coding: utf-8


from time import sleep
import unittest, random, sys
sys.path.append("./models/")
sys.path.append("./page_obj/")
print(sys.path)
from models import myunit, function
from page_obj.loginPage import login

class loginTest(myunit.MyTest):

	#测试用户登录
	def user_login_verify(self, username="", password=""):
		login(self.driver).user_login(username, password)

	def test_login1(self):
		'''
		用户名、密码错误登录
		'''
		self.user_login_verify(username='cjcha.net', password='123456')
		po = login(self.driver)
		self.assertEqual(po.user_error_hint(), "请输入正确的邮箱或手机号")
		function.insert_img(self.driver, "user_pawd_error.png")

	def test_login2(self):
		'''
		用户名、密码正确登录
		'''
		self.user_login_verify(username='cjcha2o@sogaa.net', password='123456')
		po = login(self.driver)
		self.assertEqual(po.user_login_success(), "高校邀请")
		function.insert_img(self.driver, "user_pawd_true.png")


if __name__ == '__main__':
	unittest.main()












