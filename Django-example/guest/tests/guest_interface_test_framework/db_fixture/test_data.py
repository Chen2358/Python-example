#coding: utf-8

import sys
sys.path.append('../db_fixture')
from mysql_db import DB

# 定义过去时间
past_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-100000))

# 定义将来时间
future_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()+10000))

#创建测试数据
datas = {
	#发布会数据
	'sign_event':[
		{'id': 1, 'name': '红米', '`limit`': 200, 'status': 1, 'address': '北京会展中心', 'start_time': 'past_time'},
		{'id': 2, 'name': '红米por', '`limit`': 0, 'status': 1, 'address': '北京会展中心', 'start_time': 'past_time'},
		{'id': 3, 'name': '红米5', '`limit`': 200, 'status': 0, 'address': '北京会展中心', 'start_time': 'future_time'},
	],
	#嘉宾数据
	'sign_guest':[
		{'id': 1, 'realname': 'A', 'phone': '13611001011', 'email': '13611001011@mail.com', 'sign': 1, 'event_id': 1},
		{'id': 1, 'realname': 'B', 'phone': '13611001012', 'email': '13611001012@mail.com', 'sign': 0, 'event_id': 2},
		{'id': 1, 'realname': 'C', 'phone': '13611001013', 'email': '13611001013@mail.com', 'sign': 1, 'event_id': 3},
	],
}


#将测试数据插入表
def init_data():
    DB().init_data(datas)

if __name__ == '__main__':
	init_data()















