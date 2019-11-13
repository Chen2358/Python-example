#coding: utf-8

import requests
import unittest


class GetEventListTet(unittest.TestCase):

	def setUp(self):
		self.url = 'http://localhost:8000/api/get_event_list'

	def test_get_event_id_null(self):
		r = requests.get(self.url, params={'eid': ''})
		result = r.json()
		self.assertEqual(result['status'], 10021)
		self.assertEqual(result['message'], 'parameter error')

	def test_get_event_id_error(self):
		r = requests.get(self.url, params={'eid': '900'})
		result = r.json()
		self.assertEqual(result['status'], 10022)
		self.assertEqual(result['message'], 'query result is empty')

	def test_get_event_id_success(self):
		r = requests.get(self.url, params={'eid': 4})
		result = r.json()
		self.assertEqual(result['status'], 200)
		self.assertEqual(result['message'], 'success')
		self.assertEqual(result['data']['name'], '魅族16pro')
		self.assertEqual(result['data']['address'], '北京水立方')

if __name__ == '__main__':
	unittest.main()


















































