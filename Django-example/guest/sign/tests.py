from django.test import TestCase
from sign.models import Event, Guest 
from django.contrib.auth.models import User

# Create your tests here.


class ModelTest(TestCase):

	def setUp(self):
		Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000, address='shenzhen', start_time='2016-08-31 02:18:22')
		Guest.objects.create(id=1, event_id=1, realname='alen', phone='13711001101', email='alen@mail.com', sign=False)

	def test_event_models(self):
		result = Event.objects.get(name="oneplus 3 event")
		self.assertEqual(result.address, "shenzhen")
		self.assertTrue(result.status)

	def test_guest_models(self):
		result = Guest.objects.get(phone='13711001101')
		self.assertEqual(result.realname, "alen")
		self.assertFalse(result.sign)


class IndexPageTest(TestCase):

	'''测试index登录首页'''
	def test_index_page_renders_index_template(self):
		'''测试index视图'''
		response = self.client.get('/index/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):

	'''测试登录'''
	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

	def test_add_admin(self):
		user = User.objects.get(username="admin")
		self.assertEqual(user.username, "admin")
		self.assertEqual(user.email, "admin@mail.com")

	def test_login_action_username_password_null(self):
		'''用户名密码为空'''
		test_data = {'username': '', 'password': ''}
		response = self.client.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"username or password error!", resposne.content)

	def test_login_action_username_password_error(self):
		'''用户名密码错误'''
		test_data = {'username': 'abc', 'password': '123'}
		response = self.client.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"username or password error!", resposne.content)

	def test_login_action_success(self):
		test_data = {'username': 'admin', 'password': 'admin123456'}
		response = self.client.post('/login_action/', data=test_data)
		self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):

	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		Event.objects.create(name="xiaomi5", status=1, limit=2000, address='beijing', start_time='2017-08-31 02:18:22')
		self.login_user({'username': 'admin', 'password': 'admin123456'})

	def test_event_manage_success(self):
		'''测试发布会'''
		response = self.client.post('/login_action/', data=self.login_user)
		response =  self.client.post('/event_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"xiaomi5", response.content)
		self.assertIn(b"beijing", response.content)

	def test_event_manage_search_success(self):
		'''发布会搜索'''
		response = self.client.post('/login_action/', data=self.login_user)
		response = self.client.post('/search_name/', {"name": "xiaomi5"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"xiaomi5", response.content)
		self.assertIn(b"beijing", response.conent)


class GuestManageTest(TestCase):

	'''嘉宾管理'''
	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		Event.objects.create(name="xiaomi5", status=1, limit=2000, address='beijing', start_time='2017-08-31 02:18:22')
		Guest.objects.create(realname='alen', phone='18611001101', email='alen@mail.com', sign=0, event_id=1)
		self.login_user({'username': 'admin', 'password': 'admin123456'}) 

	def test_guest_manage_success(self):
		response = self.client.post('/login_action/', data=test_data)
		response = self.client.post('/guest_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"alen", response.content)
		self.assertIn(b"18611001101", response.content)

class SignIndexActionTest(TestCase):

	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		Event.objects.create(id=1, name="xiaomi5", status=1, limit=2000, address='beijing', start_time='2017-08-31 02:18:22')
		Event.objects.create(id=2, name="oneplus4", status=1, limit=2000, address='beijing', start_time='2017-09-31 02:18:22')
		Guest.objects.create(realname='alen', phone='18611001101', email='alen@mail.com', sign=0, event_id=1)
		st.objects.create(realname='una', phone='18611001102', email='una@mail.com', sign=1, event_id=2)
		self.login_user({'username': 'admin', 'password': 'admin123456'}) 


	def test_sign_index_aciton_phone_null(self):
		'''手机号为空'''
		response = self.client.post('/login_action/',  data=self.login_user)
		response = self.client.post('/sign_index_action/1/', {"phone": ""})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"phone error.", response.content)

	def test_sign_index_action_phone_or_event_id_error(self):
		'''手机号或发布会id错误'''
		response = self.client.post('/login_action/',  data=self.login_user)
		response = self.client.post('/sign_index_action/2/', {"phone": "18611001101"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"event id or phone error.", response.conent)

	def test_sign_index_action_user_sign_has(self):
		response = self.client.post('/login_action/', data=self.login_user)
		response = self.client.post('/sign_index_action/2', {"phone": "18611001102"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"user has sign in.", response.content)

	def test_sign_index_action_sign_success(self):
		response = self.client.post('/login_action/',  data=self.login_user)
		response = self.client.post('/sign_index_action/1/', {"phone": "18611001101"})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"sign in success!", response.content)

'''
运行所有用例：
python3 manage.py test

运行sign应用下的所有用例：
python3 manage.py test sign

运行sign应用下的tests.py文件用例：
python3 manage.py test sign.tests

运行sign应用下的tests.py文件中的 GuestManageTest 测试类：
python3 manage.py test sign.tests.GuestManageTest

'''
