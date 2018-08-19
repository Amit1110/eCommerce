from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser
)

class User(AbstractBaseUser):
	email = models.EmailField(max_length = 255,unique=True)
	#full_name = models.CharField(max_length=255, blank = True, null=True)
	active = models.BooleanField(default=True)#can login
	staff = models.BooleanField(default=False)#staff user
	admin = models.BooleanField(default=False)#superuser
	timestamp = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['']

	def __Str__(self):
		return self.email
	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	@property
	def is_staff(Delf):
		return self.staff

	@property
	def is_admin(Delf):
		return self.admin

	@property
	def is_active(Delf):
		return self.active



class GuestEmail(models.Model):
	email = models.EmailField()
	active = models.BooleanField(default=True)
	update = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email