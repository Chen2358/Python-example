#coding: utf-8


from locust import HttpLocust, TaskSet, task
from random import randint

#定义用户行为
#Web接口
class UserBehavior(TaskSet):

	@task
	def user_sign(self):
		number = randint(1, 3001)
		str_phone = 13800110000 + number
		self.client.post("http://localhost:8000/api/user_sign", data={"eid": "1",
												"phone": str_phone})


class WebSiteUser(HttpLocust):
	task_set = UserBehavior
	min_wait = 3000
	max_wait = 6000














