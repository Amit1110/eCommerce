from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Cart

from products.models import Product
from billing.models import BillingProfile
from .models import Cart
from orders.models import Order

from addresses.forms import AddressForm
from addresses.models import Address

from accounts.models import GuestEmail

from accounts.forms import LoginForm, GuestForm


import stripe
STRIPE_SECRET_KEY = getattr(settings,"STRIPE_SECRET_KEY","sk_test_OBJ1L6pbEG137xczBIVLrp6n")
STRIPE_PUB_KEY = getattr(settings,"STRIPE_PUB_KEY","pk_test_ThzzgkBGhdMHqFaMi093UcFe")
stripe.api_key = STRIPE_SECRET_KEY


def cart_detail_api_view(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	products = [{
		"id": x.id,
		"url": x.get_absolute_url(),
		"name":x.name, "price":x.price} for x in cart_obj.products.all()]
	cart_data = {"products":products, "subtotal":cart_obj.subtotal, "total":cart_obj.total}
	return JsonResponse(cart_data)

def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)

	return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
	product_id = request.POST.get('product_id')

	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Show message to user")
			return redirect("cart:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added = False		
		else:	
			cart_obj.products.add(product_obj)
			added = True
	#cart_obj.products.remove(obj)
		request.session['cart_items'] = cart_obj.products.count()
	#return redirect(product_obj.get_absolute_url())
		if request.is_ajax():
			print("Ajax request") #Asynchronous JavaScript And XML / JSON
			json_data = {
				"added": added,
				"removed": not added,
				"cartItemCount": cart_obj.products.count()
			}
			return JsonResponse(json_data,status=200)
			#return JsonResponse({"message":"Error Code 400"},status_code=400)
	return redirect("cart:home")


def checkout_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	order_obj = None
	if new_obj or cart_obj.products.count()==0:
		return redirect("cart:home")
	# user = request.user
	login_form = LoginForm()

	guest_form = GuestForm()

	address_form = AddressForm()

	billing_address_id = request.session.get("billing_address_id",None)

	shipping_address_id = request.session.get("shipping_address_id",None)


	# guest_email_id = request.session.get('guest_email_id')

	# billing_profile = None
	# if user.is_authenticated():

	# 	billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)

	# elif guest_email_id is not None:

	# 	guest_email_id_obj = GuestEmail.objects.get(id = guest_email_id)
	# 	billing_profile, billing__guest_profile_created = BillingProfile.objects.get_or_create( email=guest_email_id_obj.email)
	# else:
	# 	pass
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	address_qs = None
	has_card = False
	if billing_profile is not None:
		if request.user.is_authenticated():
			address_qs = Address.objects.filter(billing_profile = billing_profile)
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)
		if shipping_address_id:
			order_obj.shipping_address_id = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id:
			order_obj.billing_address_id = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if billing_address_id or shipping_address_id:
			order_obj.save()
		has_card = billing_profile.has_card

	if request.method == "POST":
		"some checkout that order is complete"
		is_prepared = order_obj.check_done()
		if is_prepared:
			did_charge, charge_msg = billing_profile.charge(order_obj)
			if did_charge:
				order_obj.mark_paid()
				request.session['cart_items'] = 0
				del request.session['cart_id']
				return redirect("cart:success")
			else:
				print(charge_msg)
				return redirect("cart:checkout")
	'''
	update ordere_obj -- complete, paid
	del request.session['cart_id']
	redirect to success
	'''

	context ={
	"object":order_obj,
	"billing_profile":billing_profile,
	"login_form":login_form,
	"guest_form":guest_form,
	"address_form":address_form,
	"address_qs" : address_qs,
	"has_card": has_card,
	"publish_key" : STRIPE_PUB_KEY,
	}

	return render(request, "carts/checkout.html",context)


def checkout_done_view(request):
	return render(request, "carts/checkout-done.html",{})