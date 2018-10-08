#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv

url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"

#已完成的页数序号
page = 0

#打开csv文件
csv_file = open("rent.csv", "w")
#创建writer对象，指定文件与分隔符
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
	page += 1
	print("fetch: ", url.format(page=page))
	#抓取目标页面
	response = requests.get(url.format(page=page))
	#创建BeautifulSoup对象
	html = BeautifulSoup(response.text)
	#获取class=list的元素下的所有li元素
	house_list = html.select(".list > li")

	#
	if not house_list:
		break

	for house in house_list:
		#
		house_title = house.select("h2")[0].string
		#拼接地址
		house_url = "http://bj.58.com/%s" % (house.select("a")[0]["href"])
		house_info_list = house_title.split()

		#
		if "gongyu" in house_info_list[1] or "qingnianshequ" in house_info_list[1]:
			house_location = house_info_list[0]
		else:
			house_location = house_info_list[1]

		house_money = house.select(".money")[0].select("b")[0].string
		#写入一行数据
		csv_writer.writerow([house_title, house_location, house_money, house_url])
#关闭文件
csv_file.close()
