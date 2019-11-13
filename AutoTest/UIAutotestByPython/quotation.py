#-*- coding: utf-8 -*-

'''
售前代发询价
'''

import pykeyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pykeyboard import PyKeyboard
import win32gui
import win32con
import time, os


URL = 'http://192.168.1.10:8080/work'
USERNAME = 'sujia100@sogaa.net'
PASSWORD = '123456'
CUSTOMER = 'tester'
tuzhiPath = 'C:\\Users\\sogaa001\\Downloads\\询价\\1\\gear.zip'
listPath = 'C:\\Users\\sogaa001\\Downloads\\询价\\1\\geartest.xls'
INNERNAME = 'firstAutoTest'

driver = webdriver.Chrome()
driver.get(URL)

username = WebDriverWait(driver, 5, 0.5).until(
						EC.presence_of_element_located((By.ID, "login_username"))
						)

username.send_keys(USERNAME)
time.sleep(2)

password = WebDriverWait(driver, 5, 0.5).until(
						EC.presence_of_element_located((By.ID, "login_password"))
						)

password.send_keys(PASSWORD)
time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="loginForm"]/button').click()
time.sleep(3)
driver.maximize_window()
#代发询价

WebDriverWait(driver, 5, 0.5).until(
						EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/aside[1]/div/nav/ul/li[1]/a/span"))
						).click()
WebDriverWait(driver, 5, 0.5).until(
						EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/aside[1]/div/nav/ul/li[1]/ul/li[2]/a/span"))
						).click()

daifa = WebDriverWait(driver, 5, 0.5).until(
						EC.presence_of_element_located((By.XPATH, '//*[@id="mainContainer"]/div[2]/div/div/div/div[2]/div/button[3]'))
						)
daifa.click()
time.sleep(3)

# daifa_windows = driver.current_window_handle

# print(daifa_windows)
# current = current_window_handle
# print(current_window_handle)

#切换活动 窗口
driver.switch_to_window(driver.window_handles[1])
# print(driver.title)


#搜索客户
customer = driver.find_element(By.XPATH, '//*[@id="inputUserName"]').send_keys(CUSTOMER)
time.sleep(3)

search = driver.find_element(By.XPATH, '//*[@id="panel0"]/div[2]/form/div/div/div[2]/button[1]').click()
time.sleep(2)

xuanze = driver.find_element(By.XPATH, '//*[@id="table-ext-1"]/tbody/tr[2]/td[1]/div/label/span').click()
time.sleep(2)

#上传图纸零件

tuzhi_upload = driver.find_element(By.XPATH, '//*[@id="panel1"]/div[2]/div[1]/div[1]/div/div[1]/label')
tuzhi_upload.click()
time.sleep(3)

# 使用win32gui
dialog = win32gui.FindWindow('#32770', u'打开')  # 对话框
ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None) 
ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 打开按钮Button

win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, tuzhiPath)  # 往输入框输入绝对地址
win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
time.sleep(5)

#上传图纸清单
liebiao_upload = driver.find_element(By.CSS_SELECTOR, '#panel1 > div.panel-body.row.mt-lg.form-horizontal.in.collapse > div:nth-child(2) > div.col-md-12.row.mb-lg > div > div.box-placeholder.my-drop-zone.bg-user > label')
liebiao_upload.click()
# print('qingdan!!!!!!!!!!!!!!!!!!!!!!!!!!')
time.sleep(3)


#同上
dialog = win32gui.FindWindow('#32770', u'打开')  # 对话框
ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None) 
ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 打开按钮Button

win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, listPath)  # 往输入框输入绝对地址
win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
time.sleep(3)


#解析列表
jiexi= WebDriverWait(driver, 5, 0.5).until(
						EC.element_to_be_clickable((By.CSS_SELECTOR, '#panel1 > div.panel-body.row.mt-lg.form-horizontal.in.collapse > div.row > div > button'))
						)
jiexi.click()
time.sleep(3)
# print('success!')

#向下滑动
js="window.scrollTo(100,1000);"
driver.execute_script(js)
time.sleep(2)

#询价单名称
quotationName = driver.find_element(By.XPATH, '//*[@id="panel3"]/div[2]/div[1]/div[1]/div/input')
quotationName.send_keys(INNERNAME)
time.sleep(2)

#优先级
priority = driver.find_element(By.CSS_SELECTOR, '#panel3 > div.panel-body.form-horizontal.in.collapse > div:nth-child(1) > div:nth-child(2) > div > div > select')
priority.click()
time.sleep(3)

#低
priority_low = driver.find_element(By.CSS_SELECTOR, '#panel3 > div.panel-body.form-horizontal.in.collapse > div:nth-child(1) > div:nth-child(2) > div > div > select > option:nth-child(4)')
priority_low.click()
time.sleep(3)


#重大单
importantFlag = driver.find_element(By.CSS_SELECTOR, '#panel3 > div.panel-body.form-horizontal.in.collapse > div:nth-child(5) > div > div > div:nth-child(1) > label > span')
importantFlag.click()
time.sleep(3)

#是否有历史价格
historicalPriceStatus = driver.find_element(By.CSS_SELECTOR, '#panel3 > div.panel-body.form-horizontal.in.collapse > div:nth-child(6) > div > div > div:nth-child(1) > label > span')
historicalPriceStatus.click()
time.sleep(3)

#提交
doSubmit = driver.find_element(By.CSS_SELECTOR, '#panel3 > div.panel-body.form-horizontal.in.collapse > div.col-md-12.text-center > button')
doSubmit.click()
time.sleep(3)

driver.switch_to.alert.accept()