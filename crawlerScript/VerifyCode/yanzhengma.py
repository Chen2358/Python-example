# -*- coding:  utf-8 -*-

'''
#图片验证码

from PIL import Image
import pytesseract

# (1)没有偏差的验证码

image = Image.open(r'code.jpg')
text = pytesseract.image_to_string(image)
print(text)
'''

'''
#(2)有偏差的验证码，及验证码图片内多余线条干扰了识别

image = Image.open(r'code2.jpg')

#cover()传入L参数，将图片转头灰度图片
image = image.covert('L')

#传入l(数字1)参数将图片进行二值化处理
image = image.convert('1')
image.show()
text = pytesseract.image_to_string(image)
print(text)

'''
'''
#不能转化原图，先转为灰度图，再指定二值化阈值
threshold = 80
table = []
for i in raneg(256):
	if i < threshold:
		table.append(0)
	else:
		table.append(1)
image = image.point(table, '1')
image.show()
text = pytesseract.image_to_string(image)
print(text)
'''

"""


#极验滑动验证码
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
import time



EMAIL = 'test@test.com'
PASSWORD = '123456'
BORDER  = 6
INIT_LEFT = 60

class CrackGeetest(object):

	def __init__(self):
		self.url = 'https://auth.geetest.com/login'
		self.browser = webdriver.Chrome()
		self.wait = WebDriverWait(self.browser, 20)
		self.email = EMAIL
		self.password = PASSWORD

	def __del__(self):
		self.browser.close()

	def get_geetest_button(self):
		'''
		获取初始验证按钮
		'''
		button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
		return button

	#识别缺口
	def get_position(self):
		'''
		获取验证码位置
		'''
		img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
		time.sleep(2)
		location = img.location
		size = img.size
		top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'],
			location['x']+ size['width']
		return (top, bottom, left, right)


	def get_screenshot(self):
		'''
		通过截图获取验证码图片
		'''
		screenshot = self.browser.get_screenshot_as_png()
		screenshot = Image.open(BytesIO(screenshot))
		return screenshot


	def get_slider(self):
		'''
		获取滑块
		: return: 图片对象
		'''
		slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
		return slider


	def get_geetest_image(self, name='captcha.png'):
		'''
		通过截图获取验证码图片
		'''
		top, bottom, left, right = self.get_position()
		print('验证码位置', top, bottom, left, right)
		screenshot = self.get_screenshot()
		captcha = screenshot.crop((left, top, right, bottom))	#图片裁剪
		captcha.save(name)
		return captcha

	def open(self):
		'''
		打开网页输入用户名密码
		'''
		self.browser.get(self.url)
		email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
		password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
		email.send_keys(self.email)
		password.send_keys(self.password)

	def get_gap(self, image1, image2):
		'''
		获取缺口偏移量
		:param image1: 不带缺口图片
		:param iamge2: 带缺口图片
		'''
		left = 60
		for i in range(left, image1.size[0]):
			for j in range(image1.size[1]):
				if not self.is_pixel_equal(image1, image2, i, j):
					left = i
					return left
		return left

	#判断缺口
	def is_pixel_equal(self, image1, image2, x, y):
		'''
		判断两个像素是否相同
		'''
		#获取图片的像素点
		pixel1 = image1.load()[x, y]
		pixel2 = image2.load()[x, y]

		#两张图片RGB的差绝对值是否均小于定义的阈值：在阈值内则代表像素点相同
		threshold = 60
		if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
			return True
		else:
			return False


	#模拟拖动
	def get_track(self, distance):
		'''
		根据偏移量获取移动轨迹
		:param distance：偏移量
		:return：移动轨迹
		先加速后减速
		'''

		#移动轨迹
		track = []

		#当前位移
		current = 0

		#减速阈值:4/5 路程加速，1/5减速
		mid = distance * 4 / 5

		#计算间隔
		t = 0.2

		#初速度
		v = 0

		while current < distance:
			if current < mid:
				#加速度为 正2
				a = 2
			else:
				#加速度为负3
				a = -3
			#初速度 v0
			v0 = v

			#当前速度v = v0 + at
			v = v0 + a * t

			#移动距离 x = v0t + 1/2 * a * t^2
			move = v0 * t + 1 / 2 * a * t * t

			#当前位移
			current += move 
			#加入轨迹
			track.append(round(move))
		return track

	def move_to_gap(self, slider, tracks):
		'''
		拖动滑块到缺口处
		:param slider: 滑块
		:param tracks: 轨迹
		'''
		ActionChains(self.browser).click_and_hold(slider).perform()
		for x in tracks:
			ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
		time.sleep(0.5)
		ActionChains(self.browser).release().perform()

	def login(self):
		'''
		登录
		'''
		submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
		submit.click()
		time.sleep(10)
		print('Success!')

	def crack(self):
		#输入用户名密码
		self.open()
		#点击验证按钮
		button = self.get_geetest_button()
		button.click()
		#获取验证码图片
		image1 = self.get_geetest_image('captcha1.png')

		#点按呼出缺口
		slider = self.get_slider()
		slider.click()

		#获取带缺口的验证码图片
		iamge2 = self.get_geetest_image('captcha2.png')

		#获取缺口位置
		gap = self.get_gap(image1, image2)
		print('缺口位置', gap)

		#减去缺口位置
		gap -= BORDER

		#获取移动轨迹
		track = self.get_track(gap)
		print('滑动轨迹', track)

		#拖动滑块
		self.move_to_gap(slider, track)

		success = self.wait.until(
			EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
		print(success)

		#失败后重试
		if not success:
			self.crack()
		else:
			self.login()

if __name__ == '__main__':
	crack = CrackGeetest()
	crack.crack()

"""

"""
#点触验证码识别

'''
思路：
1、将验证码图片提交到平台（https://www.chaojiying.com/）
2、平台返回识别结果在图片中的位置；
3、解析坐标模拟点击

注册账号->获取PythonAPI：https://www.chaojiying.com/api-14.html
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
import time
from chaojiying import Chaojiying


EMAIL = 'test@test.com'
PASSWORD =  ''

#超级鹰用户名、密码、软件ID、验证码类型
CHAOJIYING_USERNAME = 'chen'
CHAOJIYING_PASSWORD = ''
CHAOJIYING_SOFT_ID = 893590
CHAOJIYING_KIND = 9102



#初始化
class CrackTouClick(object):

	def __init__(self):
		self.url = 'http://admin/touclick.com/login.html'
		self.browser = webdriver.Chrome()
		self.wait = WebDriverWait(self.browser, 20)
		self.email = EMAIL
		self.password = PASSWORD
		self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

	def __del__(self):
		self.browser.close()

	#获取验证码
	def open(self):
		self.browser.get(self.url)
		email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
		password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
		email.send_keys(self.email)
		password.send_keys(self.password)

	def get_touclick_button(self):
		'''
		获取初始验证按钮
		'''
		button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'touclick-hod-wrap')))
		return button

	def get_touclick_element(self):
		'''
		获取验证图片对象
		'''
		element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'touclick-pub-content')))
		return element

	def get_position(self):
		'''
		获取验证码位置
		'''
		element = self.get_touclick_element()
		time.sleep(2)
		location = element.location
		size = element.size
		top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
		return (top, bottom, left, right)

	def get_screenshot(self):
		'''
		获取网页截图
		'''
		screenshot = self.browser.get_screenshot_as_png()
		screenshot = Image.open(BytesIO(screenshot))
		return screenshot

	def get_touclick_image(self, name='captcha.png'):
		'''
		获取验证码图片
		'''
		top, bottom, left, right = self.get_position()
		print('验证码位置', top, bottom, left, right)
		screenshot = self.get_screenshot()
		captcha = screenshot.crop((left, top, right, bottom))
		captcha.save(name)
		return captcha

	def get_points(self,  captcha_result):
		'''
		解析识别结果
		:param captcha_result: 识别结果
		:return: 转化后的结果
		'''
		groups = captcha_result.get('pic_str').split('|')
		locations = [[int(number) for number in group.split(',')] for group in groups]
		return locations

	def touch_click_words(self, locations):
		'''
		点击验证图片
		:param locations: 点击位置
		'''
		for location in locations:
			print(location)
			ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0], location[1]).click().peroform()
		time.sleep(1)

	def touch_click_verify(self):
		'''
		点击验证按钮
		'''
		button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'touclick-pub-submit')))
		button.click()

	def login(self):
		'''
		登录
		'''
		submit = self.wait.until(EC.element_to_be_clickable((By.ID, '_submit')))
		button.click()
		time.sleep(10)
		print('登录成功')

	def crack(self):
		'''
		破解入口
		'''
		self.open

		button = self.get_touclick_button()
		button.click()
		
		#将图片传给超级鹰后台
		image = self.get_touclick_image()
		bytes_array = BytesIO()
		image.save(bytes_array, format='PNG')

		#识别验证码
		result = self.chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_KIND)
		print(result)
		locations = self.get_points(result)
		self.touch_click_words(locations)
		self.touch_click_verify()
		#
		success = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'touclilck-hod-note'), '验证成功'))
		print(success)

		#失败后重试
		if not success:
			self.crack()
		else:
			self.login()
if __name__ == '__main__':
	crack = CrackTouClick()
	crack.crack()

"""

#宫格验证码
#思路：用模板匹配，将一些识别目标提前保存并做好标记，称为模板

import time
from io import BytesIO
from PIL import Image
from os import listdir
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = '1430535115@qq.com'
PASSWORD = 'qq@443120'
TEMPLATES_FOLDER = 'templates/'

#获取模板:模板命名：4132代表从第四个点到第一个到第三个最后到第二个
class CrackWeiboSlider(object):

	def __init__(self):
		self.url = 'https://passport.weibo.cn/signin/login'
		self.browser = webdriver.Chrome()
		self.wait = WebDriverWait(self.browser, 20)
		self.username = USERNAME
		self.password = PASSWORD

	def __del__(self):
		self.browser.close()

	def open(self):
		self.browser.get(self.url)
		username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
		password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
		submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
		username.send_keys(self.username)
		password.send_keys(self.password)
		submit.click()

	def get_position(self):
		'''
		获取验证码位置
		'''
		try:
			img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'patt-shadow')))
		except TimeoutException:
			print('未出现验证码')
			self.open()
		time.sleep(2)
		location = img.location
		size = img.size
		top, bottom,left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
		return (top, bottom, left, right)

	def get_screenshot(self):
		'''
		获取网页截图
		'''
		screenshot = self.browser.get_screenshot_as_png()
		screenshot = Image.open(BytesIO(screenshot))
		return screenshot

	def get_image(self,name='captcha.png'):
		'''
		获取验证码图片
		'''
		top, bottom, left, right = self.get_position()
		print('验证码位置', top, bottom, left, right)
		screenshot =self.get_screenshot()
		captcha = screenshot.crop((left, top, right, bottom))
		captcha.save(name)
		return captcha

	def is_pixel_equal(self, image1, image2, x, y):
		'''
		判断两个像素是否相同
		:param image1: 图片1
		:param image2:图片2
		:param x: 位置x
		:param y: 位置y
		'''
		#获取图片的像素点
		pixel1 = image1.load()[x, y]
		pixel2 = image2.load()[x, y]

		#两张图片RGB的差绝对值是否均小于定义的阈值：在阈值内则代表像素点相同
		threshold = 20
		if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
			return True
		else:
			return False

	def same_image(self, image, template):
		'''
		识别相似验证码
		:param image: 待识别验证码
		:param template: 模板
		'''
		threshold = 0.99
		count = 0
		for x in range(image.width):
			for y in range(image.height):
				#判断像素是否相同
				if self.is_pixel_equal(iamge, template, x, y):
					count += 1
		result = float(count) / (image.width * image.height)
		if result > threshold:
			print('成功匹配')
			return True
		return False

	def detect_imgage(self, image):
		'''
		匹配图片
		'''
		for template_name  in listdir(TEMPLATES_FOLDER):
			print('正在匹配', template_name)
			template = Image.open(TEMPLATES_FOLDER + template_name)
			if self.same_image(image, template):
				'''
				返回顺序
				'''
				numbers = [int(number) if number in list(template_name.split('.')[0])]
				print('拖动顺序', numbers)
				return numbers

	def move(self, numbers):
		'''
		根据顺序拖动
		'''
		#获取四个按点
		circles = self.browser.find_elements_by_css_selector('.patt-wrap .patt-circ')
		dx = dy = 0
		for index in range(4):
			circle = circles[numbers[index] - 1]
			#如果是第一次循环
			if index == 0:
				#点击第一个按点
				ActionChains(self.browser).move_to_element_with_offset(circle,  circle.size['width'] / 2,
					circle.size['height'] / 2).click_and_hold().perform()
			else:
				#小幅移动次数
				times = 30
				#拖动
				for i in range(times):
					ActionChains(self.browser).move_by_offset(dx / times,  dy / times).perform()
					time.sleep(1 / times)
			#如果是最后一次循环
			if index == 3:
				#松开鼠标
				ActionChains(self.browser).release().perform()
			else:
				#计算下一次偏移
				dx = circles[numbers[index + 1] - 1].location['x'] - circle.location['x']
				dy = circles[numbers[index + 1] - 1].location['y'] - circle.location['y']


	def crack(self):
		'''
		破解入口
		'''
		self.open()
		#
		image = self.get_image('captcha.png')
		numbers = self.detect_imgage(image)
		self.move(numbers)
		time.sleep(10)
		print('识别结束')



if __name__ == '__main__':
	crack = CrackWeiboSlider()
	crack.crack()