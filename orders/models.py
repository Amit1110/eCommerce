from django.db import models
from django.db.models.signals import pre_save,post_save
import math
from carts.models import Cart

from billing.models import BillingProfile

from ecommerce.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
	('created', 'Created'),
	('shipped', 'Shipped'),
	('paid', 'Paid'),
	('refunded', 'Refunded'),
		)


class OrderManager(models.Manager):
	def new_or_get(self, billing_profile, cart_obj):
		created = False
		order_qs = self.get_queryset().filter(billing_profile = billing_profile,cart = cart_obj,active=True)
		if order_qs.count()==1:
			order_obj = order_qs.first()
		else:
			order_obj = self.model.objects.create(billing_profile=billing_profile,cart=cart_obj)
			created = True
		return order_obj, created

class Order(models.Model):
	# pk, id
	order_id = models.CharField(max_length=120,blank=True)# random , unique
	billing_profile = models.ForeignKey(BillingProfile,null=True, blank=True)
	#shipping address
	#billing address
	cart = models.ForeignKey(Cart)
	status = models.CharField(max_length=120, default = 'created', choices = ORDER_STATUS_CHOICES)
	shipping_total = models.DecimalField(default = 5.99,max_digits = 100,decimal_places=2)
	total = models.DecimalField(default = 0.0,max_digits = 100,decimal_places=2)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.order_id

	objects = OrderManager()

	def update_total(self):
		cart_total = self.cart.total
		shipping = self.shipping_total
		new_total = math.fsum([cart_total ,shipping])
		formatted_total = format(new_total,'.2f')
		#print(type(new_total))
		self.total = formatted_total
		self.save()
		return new_total


def pre_save_create_order_id(sender,instance,*args, **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id_generator(instance)
	qs = Order.objects.filter(cart = instance.cart).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
	if not created:	
		cart_obj = instance
		cart_total = cart_obj.total
		cart_id = cart_obj.id
		qs = Order.objects.filter(cart__id=cart_id)
		if qs.count()==1:
			order_obj = qs.first()
			order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender,instance,created, *args, **kwargs):
	if created:
		instance.update_total()

post_save.connect(post_save_order,sender=Order)