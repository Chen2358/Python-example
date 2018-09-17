#!/usr/bin/env python3
# coding: utf-8

import requests
import itchat

KEY = '8edce3ce905a4c1dbb965e6b35c3834d'

def get_response(msg):

	apiUrl = 'http://www.tuling123.com/openapi/api'
	data = {
	'key'		: KEY,
	'info'		: msg,
	'userid'	: 'wechat-robot',
	}
	try:
		r = requests.post(apiUrl, data=data).json()
		#
		return r.get('text')
	#
	#
except:
	return

@itcht.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
	defaultReply = 'I receiver: ' + msg['Text']
	#
	reply = get_response(msg['Text'])
	#
	return reply or defaultReply

itchat.auto_login(hotReload=True)
itchat.run()