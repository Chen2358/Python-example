#!/usr/bin/env python3
# coding: utf-8

import itchat

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
	print(msg['Text'])

itchat.auto_login()
#itchat.auto_login(hotReload=True)
itchat.send(u'fasongxiaoxi', 'toUserName')
itchat.run()