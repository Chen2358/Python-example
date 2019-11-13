#coding: utf-8
    
import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data

class UserSignTest(unittest.TestCase):
    ''' 获得嘉宾列表 '''

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/user_sign/"

    def tearDown(self):
        print(self.result)

    def test_user_sign_all_null(self):
    	payload = {'eid', '', 'phone': ''}
    	r = requests.post(self.base_url, data=payload)
    	self.result = r.json()
    	self.assertEqual(self.result['status'], 10021)
    	self.assertEqual(self.result['message'], 'parameter error')

    def test_user_sign_eid_error(self):
    	payload = {'eid', '900', 'phone': ''}
    	r = requests.post(self.base_url, data=payload)
    	self.result = r.json()
    	self.assertEqual(self.result['status'], 10022)
    	self.assertEqual(self.result['message'], 'event id null')

    def test_user_sign_status_close(self):
    	payload = {'eid', '1', 'phone': '15626231223'}
    	r = requests.post(self.base_url, data=payload)
    	self.result = r.json()
    	self.assertEqual(self.result['status'], 10023)
    	self.assertEqual(self.result['message'], 'event status is not available')

    def test_user_sign_time_start(self):
    	payload = {'eid', '3', 'phone': '15626231223'}
    	r = requests.post(self.base_url, data=payload)
    	self.result = r.json()
    	self.assertEqual(self.result['status'], 10024)
    	self.assertEqual(self.result['message'], 'event has started')

    def test_user_sign_phone_error(self):
    	payload = {'eid', '3', 'phone': '15626231220'}
    	r = requests.post(self.base_url, data=payload)
    	self.result = r.json()
    	self.assertEqual(self.result['status'], 10025)
    	self.assertEqual(self.result['message'], 'user phone null')

    def test_user_sign_eid_phone_error(self):
    	payload = {'eid', '4', 'phone': '15626231223'}
    	r = requests.post(self.base_url, data=payload)
    	self.result = r.json()
    	self.assertEqual(self.result['status'], 10026)
    	self.assertEqual(self.result['message'], 'user did not participate in  the conference')

    def test_user_sign_has_sign_in(self):
    	payload = {'eid', '1', 'phone': '15626231223'}
    	r = requests.post(self.base_url, data=payload)
    	self.result = r.json()
    	self.assertEqual(self.result['status'], 10027)
    	self.assertEqual(self.result['message'], 'user has sign in')

    def test_user_sign_success(self):
    	payload = {'eid', '5', 'phone': '13611001011'}
    	r = requests.post(self.base_url, data=payload)
    	self.result = r.json()
    	self.assertEqual(self.result['status'], 200)
    	self.assertEqual(self.result['message'], 'sign success')



if __name__ == '__main__':
    test_data.init_data() # 初始化接口测试数据
    unittest.main()