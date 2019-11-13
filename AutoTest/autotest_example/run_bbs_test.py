# coding: utf-8

from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import unittest
import time
import os


#发送邮件
def send_mail(file_new):
	f = open(file_new, 'rb')
	mail_body = f.read()
	f.close()

	msg = MIMEText(mail_body, 'html', 'utf-8')
	msg['Subject'] = Header("自动化测试报告", 'utf-8')

	smtp = smtplib.SMTP()
	smtp.connect("smtp.126.com")
	smtp.login("testusername@126.com", "123456")
	smtp.sendmail("test@126.com", "receive@126.com", mgs.as_string())
	smtp.quit()
	print('email has send out!')

#朝朝测试报告目录，查找最新报告文件
def new_report(testreport):
	lists = os.listdir(testreport)
	lists.sort(key=lambda fn: os.path.getmtime(testreport + "\\" + fn))
	file_new = os.path.join(testreport, lists[-1])
	print(file_new)
	return file_new

if __name__ == '__main__':
	now = time.strftime("%Y-%m-%d %H_%M_%S")
	filename = './bbs/report/' + now + 'result.html'
	fp = open(filename, 'wb')
	runner = HTMLTestRunner(stream=fp,
							title='space 登录自动化测试报告',
							description='环境: windows 10 浏览器: chrome')

	discover = unittest.defaultTestLoader.discover('./bbs/test_case', pattern='*_sta.py')

	runner.run(discover)
	fp.close()
	file_path = new_report('./bbs/report/')
	send_mail(file_path)
















