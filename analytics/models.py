from django.conf import settings
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
	user = models.ForeignKey(User,blank=True,null=True) #user instance instance.id
	ip_address = models.CharField(max_length=220, blank = True, null=True) #IP Field
	content_type = models.ForeignKey(ContentType) #Product, Order, Cart, etc
	object_id = models.PositiveIntegerField() # user id, Product id ,Cart id, etc
	content_object = GenericForeignKey('content_type','object_id') # Product Instance
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "%s viewed on %s" %(self.content_object, self.timestamp)

	class Meta:
		ordering = ['-timestamp'] # most recent first
		verbose_name = 'Object Viewed'
		verbose_name_plural = 'Objects viewed'