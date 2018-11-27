import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db, fake
from app.models import Role, User, Post

class SeleniumTestCase(TestCase):

	client = None

	@classmethod
	def setUpClass(cls):
		#start Chrome
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		try:
			cls.client = webdriver.Chrome(chrome_options=options)
		except:
			pass

		#skip these tests if the browser could not be started
		if cls.client:
			#create the application
			cls.app = create_app('testing')
			cls.app_context = cls.app.app_context()
			cls.app_context.push()

			# suppress logging to keep unittest output clean
			import logging
			logger = logging.getLogger('werkzeug')
			logger.setLevel('ERROR')

			#create the database and populate with some fake daa
			db.create_all()
			Role.insert_roles()
			fake.users(10)
			fake.posts(10)

			#add an administrator user
			admin_role = Role.query.filter_by(name='Administrator').first()
			admin = User(email='admin@test.com',
						 username='testuser',password='admin',
						 role=admin_role, confirmed=True)
			db.session.add(admin)
			db.session.commit()

			#start the Flask server in thread
			cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'debug': False})
			cls.server_thread.start()

			#
			time.sleep(1)

	@classmethod
	def tearDownClass(cls):
		if cls.client:
			#
			cls.client.get('http://localhost:5000/shutdown')
			cls.client.quit()
			cls.server_thread.join()

			#
			db.drop_all()
			db.session.remove()

			#
			cls.app_context.pop()

	def setUp(self):
		if not self.client:
			self.skipText('Web browser not available')

	def tearDown(self):
		pass

	def test_admin_home_page(self):
		#
		self.client.get('http://localhost:5000')
		self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))

		#
		self.client.find_element_by_link_text('Log In').click()
		self.assertIn('<h1>Login<>/h1', self.client.page_source)

		#
		self.client.find_element_by_name('email').send_keys('test@qq.com')
		self.client.find_element_by_name('password').send_keys('test')
		self.client.find_element_by_name('submit').click()
		self.assertTrue(re.search('Hello,\s+testuser!', self.client.page_source))

		#
		self.client.find_element_by_link_text('Profile').click()
		self.assertIn('<h1>testuser</h1>', self.client.page_source)
