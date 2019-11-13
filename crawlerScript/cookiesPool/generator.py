#-*- coding: utf-8 -*-

'''
生成模块
'''

#找出还没对应Cookies的账号，逐个获取Cookies
for username in accounts_usernames:
	if not username in cookies_usernames:
		password = self.accounts_db_get(username)
		print('正在生成Cookies', '账号', username, '密码', password)
		result = self.new_cookies(username, password)


def get_cookies(self):
	return self.browser.get_cookies()

def main(self):
	self.open()
	if self.password_error():
		return {
			'status': 2,
			'content': '用户名或密码错误'
		}
	#如果不用验证码直接登录成功
	if self.login_successfully():
		cookies = self.get_cookies()
		return {
			'status': 1,
			'content': cookies
		}
	#获取验证码图片
	image = self.get_images('captcha.png')
	numbers = self.detect_image(image)
	self.move(numbers)
	if self.login_successfully():
		cookies = self.get_cookies()
		return {
			'status': 1,
			'content': cookies
		}
	else:
		return {
			'status': 3,
			'content': '登录失败'
		}



