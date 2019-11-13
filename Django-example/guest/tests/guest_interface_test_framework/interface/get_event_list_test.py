#coding: utf-8

import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data


class GetEventListTest(unittest.TestCase):

	def setUp(self):
		self.base_url = 'http://127.0.0.1:8000/api/get_event_list/'

	def tearDown(self):
		print(self.result)

	def test_get_event_list_eid_error(self):
		'''eid=900 查询结果为空'''
		r = requests.get(self.base_url, params={'eid': 900})
		self.result = r.json()
		self.assertEqual(self.result['status'], 10022)
		self.assertEqual(self.result['message'], 'query result is empty')


	def test_get_event_list_eid_error(self):
		'''eid=1 查询成功'''
		r = requests.get(self.base_url, params={'eid': 1})
		self.result = r.json()
		self.assertEqual(self.result['status'], 200)
		self.assertEqual(self.result['message'], 'success')
		self.assertEqual(self.result['data']['name'], u'红米Pro发布会')
		self.assertEqual(self.result['data']['address'], u'北京会展中心')

	def test_get_event_list_eid_error(self):
		'''关键字 查询结果为空'''
		r = requests.get(self.base_url, params={'name': 'abc'})
		self.result = r.json()
		self.assertEqual(self.result['status'], 10022)
		self.assertEqual(self.result['message'], 'query result is empty')

	def test_get_event_list_eid_error(self):
		'''关键字 模糊查询'''
		r = requests.get(self.base_url, params={'name': '小米'})
		self.result = r.json()
		self.assertEqual(self.result['status'], 10022)
		self.assertEqual(self.result['message'], 'success')
		self.assertEqual(self.result['data']['name'], u'小米5发布会')
		self.assertEqual(self.result['data']['address'], u'小米5发布会')


if __name__ == '__main__':
	test_data.init_data()
	unittest.main()