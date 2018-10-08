#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib
import urllib.request as urllib2
import http.cookiejar as cookielib


url = 'http://localhost:8000/polls/login'
url2 = 'http://localhost:8000/polls/date'
values = {
	'name': 'shiyanlou',
	'pwd': 'shiyanlou',
	'commit': 'Login'
}

headers = {'Referer': 'http://localhost:8000/polls/show_login'}
request = urllib2.Request(url, data=urllib.parse.urlencode(values).encode(encoding='UTF-8'), headers=headers)

cookies = cookielib.MozillaCookieJar('my_cookies.txt')
cookie_handler = urllib2.HTTPCookieProcessor(cookies)
opener = urllib2.build_opener(cookie_handler)

response = opener.open(request)
response2 = opener.open(url2)
cookies.save()
print(response2.code)
print(response2.read())