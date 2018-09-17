#!/usr/bin/env python3
# coding: utf-8

import requests
import itchat

#Tuling Key 用于与图灵服务器鉴权
KEY = '8edce3ce905a4c1dbb965e6b35c3834d'

def get_response(msg):
	#构造发送数据
	apiUrl = 'http://www.tuling123.com/openapi/api'
	data = {
	'key'		: KEY,
	'info'		: msg,	#发送的消息
	'userid'	: 'wechat-robot',	#任意
	}
	try:
		r = requests.post(apiUrl, data=data).json()
		#字典的ge 方法在字典没有‘text’值的时候回返回None 而不会抛出异常
		return r.get('text')
	except:
		return

@itcht.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
	#为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
	defaultReply = 'I receiver: ' + msg['Text']
	#如果图灵Key有问题，那么reply将会是None
	reply = get_response(msg['Text'])
	# a or b ，如果a有内容则返回a,否则返回b
	return reply or defaultReply

itchat.auto_login(hotReload=True)
itchat.run()
