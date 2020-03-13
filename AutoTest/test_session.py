#coding: utf-8


"""
session关联接口
"""

import requests

#1、登录
url = "http://192.168.1.166:8080/jenkins/j_acegi_security_check"
addItem_url = "http://192.168.1.166:8080/view/all/createItem"
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
}

data = {
	"j_username": "admin",
	"j_password": "30e8c4be2a324b10a72b10e6b3ef3700",
	"from":	"/",
	"Submit": "Sign in",
	"remember_me": "on"
}

s = requests.session()
r = s.post(url, headers=headers, data=data)
# print(r.status_code)
# print(r.content.decode('utf-8'))

#2、新建任务
#表单数据
body = {
	"name":	"autotest2",
	"mode":	"hudson.model.FreeStyleProject",
	"json":	{
		"name": "autotest2",
		"mode": "hudson.model.FreeStyleProject"
	}
}

addItem = s.post(addItem_url, data=body, verify=False)
print(addItem.status_code)
print(addItem.content.decode('utf-8'))
