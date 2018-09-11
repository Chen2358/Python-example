#/usr/bin/env python3
#-*- coding: utf-8 -*-

import checkPwd
import unittest


class TestCheck(unittest.TestCase):
	
	def test_regular(self):
		rv = checkPwd.password('qwertyu')
		self.assertTrue(repr(rv) == True)
		self.assertTrue('guize' in rv.message)

	def test_by_step(self):
		rv= checkPwd.password('ancdefg')
		self.assertTrue(repr(rv) == 'simple')
		self.assertTrue('guize' in rv.message)

	def test_common(self):
		rv = checkPwd.password('password')
		self.assertTrue(repr(rv) == 'simple')
		self.assertTrue('changjian' in rv.message)

	def test_medium(self):
		rv = checkPwd.password('tdnwh01')
		self.assertTrue(repr(rv) == 'medium')
		self.assertTrue('bugouqiang' in rv.message)

	def test_strong(self):
		rv = checkPwd.password('tdnwwwh01.')
		self.assertTrue(repr(rv) == 'strong')
		self.assertTrue('wanmei' in rv.message)

	#
	def test_email(self):
		rv =checkPwd.Email('123@qq.com')
		self.assertEqual(rv.isValidEmail(), True)

	#
	def test_emailType(self):
		rv = checkPwd.Email('123@qq.com')
		type = 'qq' or '163' or 'gmail' or '126' or 'sina'
		self.assertEqual(rv.getEmailType(), type)

if __name__ == '__main__':
	unittest.main()