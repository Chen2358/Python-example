#coding: utf-8

import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data


class AddEventTest(unittest.TestCase):

	'''添加发布会'''
	def setUp(self):
		self.base_url = 'http://127.0.0.1:8000/api/add_event/'

	def tearDown(self):
		print(self.result)

	def test_add_event_all_null(self):
		'''所有参数为空'''
		payload = {'eid':'', '':'', 'limit':'', 'address':'', 'start_time':''}
		r = requests.get(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 10021)
		self.assertEqual(self.result['message'], 'parameter error')

	def test_add_event_eid_exist(self):
		'''id已存在'''
		payload = {'eid':1, 'name':'一加4发布会', 'limit':'200', 'address':'深圳宝体', 'start_time':'2019-08-09 12:00:00'}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 10022)
		self.assertEqual(self.result['message'], 'event id already exists')

	def test_add_event_name_exist(self):
		'''name已存在'''
		payload = {'eid':5, 'name':'华为P20发布会', 'limit':'200', 'address':'深圳宝体', 'start_time':'2019-08-09 12:00:00'}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 10023)
		self.assertEqual(self.result['message'], 'event name already exists')

	def test_add_event_date_type_error(self):
		'''时间格式错误'''
		payload = {'eid':1, 'name':'华为P20发布会', 'limit':'200', 'address':'深圳宝体', 'start_time':'2019'}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 10024)
		self.assertIn('start_time format error.', self.result['message'])

	def test_add_event_success(self):
		payload = {'eid':5, 'name':'华为P20发布会', 'limit':'200', 'address':'深圳宝体', 'start_time':'2019-08-09 12:00:00'}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 200)
		self.assertEqual(self.result['message'], 'add event success')

if __name__ == '__main__':
	test_data.init_data()		#初始化数据
	unittest.main()