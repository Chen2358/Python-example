#coding: utf-8


import time, sys
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest
from db_fixture import test_data

#指定测试用例目录
test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')

if __name__ == '__main__':
	test_data.init_data()

	now = time.strftime("%Y-%m-%d %H_%M_%S")
	filename = './report/' + now + '_result.html'
	fp = open(filename, 'wb')
	runner = HTMLTestRunner(steam=fp,
							title='Guest Manage System Interface Test Report',
							descrription='Implementation Example with: ')

	runner.run(discover)
	fp.close()