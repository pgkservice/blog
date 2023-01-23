from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField

class User(AbstractUser):

	profile = models.ImageField(upload_to="profiles/", null=True, blank=True)
	phone_number = models.CharField(max_length=20,blank=True, null=True)
	about_yourself = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.username

