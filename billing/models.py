from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save,post_save

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

# abc@gmail.com -> 10000 billing profiles
# user abc@gmail.com -> 1 billing profile

import stripe

stripe.api_key = "sk_test_OBJ1L6pbEG137xczBIVLrp6n"

class BillingProfileManger(models.Manager):
	def new_or_get(self,request):
		user = request.user
		guest_email_id = request.session.get('guest_email_id')

		billing_profile = None
		created = False
		obj = None
		if user.is_authenticated():

			obj, created = self.model.objects.get_or_create(user=user, email=user.email)

		elif guest_email_id is not None:
			
			guest_email_id_obj = GuestEmail.objects.get(id = guest_email_id)
			obj, created = self.model.objects.get_or_create( email=guest_email_id_obj.email)
		else:
			pass
		return obj, created

class BillingProfile(models.Model):
	user = models.OneToOneField(User, blank=True,null=True)
	email = models.EmailField()
	active = models.BooleanField(default=True)
	update = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	customer_id = models.CharField(max_length=120,null=True,blank=True)
	#customer_id in stripe/BrainTree

	def __str__(self):
		return self.email

	objects = BillingProfileManger()

def billing_profile_created_receiver(sender,instance, *args,**kwargs):
	if not instance.customer_id and instance.email:
		print("Actual API call to Stripe")
		customer = stripe.Customer.create(
				email = instance.email
			)
		print(customer)
		instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver,sender=BillingProfile)


def user_created_receiver(sender,instance, created ,*args, **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user=instance, email = instance.email)


post_save.connect(user_created_receiver, sender = User)