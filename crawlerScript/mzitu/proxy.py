# -*- coding: utf-8 -*-
import re
import requests

iplist = []
html = requests.get("http://haoip.cc/tiqu.html")
iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)
for i in iplistn:
	i = re.sub('\n', '', ip)
	iplist.append(i.strip())
	print(i.strip())
print(iplist)