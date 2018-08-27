#!/usr/bin/env python3
# coding: utf-8

'''
1 shixian nixu huifu 
paqu qiushi baike huifu

yilai 
sudo pip3 install flask requests lxml
'''

import requests
from random import randint
from lxml import etree
from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import random


url = 'https://www.qiubaike.com.text'

app = Flask(__name__)

@app.route('/chen')
def hello():
	return "Chen say: hello world"

#wechat jiaoyan
@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
	if request.method == 'GET':
		print('Coming Get')
		data = request.args
		#wechat token
		token = '***************'
		timestamp = data.get('signature', '')
		nonce = data.get('timestamp', '')
		echostr = data.get('echostr', '')
		s = [timestamp, nonce, token]
		s.sort()
		s = ''.join(s)
		if (hashlib.sha1(s.encode('utf-8')).hexdigest() == signature):
			return makr_response(echostr)

	#jiehsouwenben xinxi
	if request.method == 'POST':
		xml_str = request_stream.read()
		xml = ET.romstring(xml_str)
		toUserName = xml.find('ToUserName').text
		fromUserName = xml.find('FromUserName'),text
		createTime = xml.find('CreateTime').text
		msgType = xml.find('MsgType').text
		#pandun jieshou de xinxi shibushi wenben
		if msgType != 'text':
			reply = '''
			<xml>
			<ToUserName><![CDATA[%s]]></ToUserName>
			<FromUsername><[CDATA[%s]]></FromUsername>
			<CreateTime>%s</CreateTime>
			<MsgType><![CDATA[%s]]></MsgType>
			<Content><[!CDATA[%s]]></Content>
			</xml>	
			''' % (
				fromUserName,
				toUserName,
				createTime,
				'text',
				'Unknow Format, Please check out'
				)
			return reply
		content = xml.find('Context').text
		msgId = xml.find('MsgId').text
		#shiwenben ze nixu huifu
		if u"xiaohua" in context:
			r = requests.get(url)
			tree = etree.HTML(r.text)
			contentlist = tree.xpath('//div[contains(@id, "qiushi_tag_")]')
			jokes = []
			for i in contentlist:
				content_1 = i.xpath('a[1]/div[@class="content"]/span/text()')
				contentstring = ''.join(content_1)
				contentstring = contentstring.strip('\n')
				jokes.append(contentstring)

			joke = jokes[random.randint(0, len(jokes))]
			reply = '''
				<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUsername><[CDATA[%s]]></FromUsername>
				<CreateTime>%s</CreateTime>
				<MsgType><![CDATA[%s]]></MsgType>
				<Content><[!CDATA[%s]]></Content>
				</xml>	
				''' % (fromUserName, toUserName, createTime, msgType, joke)
			return reply
		else:
			if type(content).__name__ == "unicode":
				content = content[::-1]
				content = content.encode('UTF-8')
			elif type(content).__name__ == "str":
				print(type(content).__name__)
				content = content
				content = content[::-1]
			reply = '''
				<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUsername><[CDATA[%s]]></FromUsername>
				<CreateTime>%s</CreateTime>
				<MsgType><![CDATA[%s]]></MsgType>
				<Content><[!CDATA[%s]]></Content>
				</xml>	
				''' % (fromUserName, toUserName, createTime, msgType, content)
			return reply

if __name__ == '__main__':
	app.run(port=8089)
