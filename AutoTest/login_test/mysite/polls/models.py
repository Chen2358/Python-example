from __future__ import unicode_literals

import uuid
from django.db import models

class User(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.TextField()
	pwd = models.TextField()

	def __str__(self):
		return ''.join([self.name,':',self.pwd])
