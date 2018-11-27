import re
import unittest
from app import create_app, db
from app.models import User, Role

class FlaskClientTestCase(unittest.TestCase):


	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		Role.insert_roles()
		self.client = self.app.test_client(use_cookies=True)

	def teatDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_home_page(self):
		response = self.client.get(url_for('main.index'))
		self.assertTrue('Stranger' in response.get_data(as_text=True))

	def test_register_and_login(self):
		#register
		response = self.client.post(url_for('auth.register'), data={
			'email': 'test@qq.com',
			'username': 'testuser',
			'password': 'test',
			'password2': 'test',
			})
		self.assertTrue(response.status_code == 302)

		#login  with new account
		response = self.clien.post(url_for('auth.login'), data={
			'email': 'test@qq.com',
			'password': 'test'
			}, follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue(re.search('Hellow, \s+testuser', data))
		self.assertTrue('You have not confiremed your account yet' in data)

		#send confimed token
		user = User.query.filter_by(email='test@qq.com').first()
		token = user.generate_confirmation_token()
		response = self.clien.get(url_for('auth.confirm', token=token), follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue('You have confirmed your account'  in  data)

		#logout
		response = self.clien.get(url_for('auth.logout'), follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue('You have been logged out' in data)
