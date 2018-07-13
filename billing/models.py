from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save,post_save

User = settings.AUTH_USER_MODEL

# abc@gmail.com -> 10000 billing profiles
# user abc@gmail.com -> 1 billing profile

class BillingProfile(models.Model):
	user = models.OneToOneField(User, blank=True,null=True)
	email = models.EmailField()
	active = models.BooleanField(default=True)
	update = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	#customer_id in stripe/BrainTree

	def __str__(self):
		return self.email

# def billing_profile_created_receiver(sender,instance,created, *args,**kwargs):
# 	if created:
# 		print("Actual API call to Stripe/Braintree")
# 		instance.customer_id = newID
# 		instance.save()


def user_created_receiver(sender,instance, created ,*args, **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user=instance, email = instance.email)


post_save.connect(user_created_receiver, sender = User)