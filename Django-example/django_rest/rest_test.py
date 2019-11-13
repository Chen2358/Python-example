#coding: utf-8

import unittest
import requests, json

class UserTest(unittest.TestCase):

	def setUp(self):
		self.base_url = 'http://127.0.0.1:8000/users'
		self.auth = ('admin', 'admin123456')

	def test_user1(self):
		r = requests.get(self.base_url +'/1', auth=self.auth)
		# print(r.text)
		result = json.loads(r.text)
		self.assertEqual(result['username'], 'admin')
		self.assertEqual(result['email'], 'admin@mail.com')

	def test_user2(self):
		r = requests.get(self.base_url +'/2', auth=self.auth)
		result = json.loads(r.text)
		self.assertEqual(result['username'], 'tom')
		self.assertEqual(result['email'], 'tom@mail.com')

	def test_user3(self):
		r = requests.get(self.base_url +'/3', auth=self.auth)
		result = json.loads(r.text)
		self.assertEqual(result['username'], 'jack')
		self.assertEqual(result['email'], 'jack@mail.com')


class GroupsTest(unittest.TestCase):

	def setUp(self):
		self.base_url = 'http://127.0.0.1:8000/groups'
		self.auth = ('admin', 'admin123456')

	def test_groups1(self):
		r = requests.get(self.base_url + '/1', auth=self.auth)
		result = json.loads(r.text)
		self.assertEqual(result['name'], 'test')

	def test_groups2(self):
		r = requests.get(self.base_url + '/2', auth=self.auth)
		result = json.loads(r.text)
		self.assertEqual(result['name'], 'developer')


if __name__ == '__main__':
	unittest.main()








































