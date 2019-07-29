#-*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstracUser
from django.db import models

class User(AbstracUser):

	GENDER_CHOICES = (
		('M', 'man'),
		('F', 'women'),
	)
	nickname = models.CharField(blank=True, null=True, max_length=20)
	avatar = models.CharField(upload_to='avatar/')
	mobile = models.CharField(blank=True, null=True, max_length=13)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
	subscribe = models.BooleanField(default=False)

	class Meta:
		db_table = "v_user"
