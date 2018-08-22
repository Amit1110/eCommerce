from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url
import stripe




stripe.api_key = "sk_test_OBJ1L6pbEG137xczBIVLrp6n"
STRIPE_PUB_KEY = "pk_test_ThzzgkBGhdMHqFaMi093UcFe"

def payment_method_view(request):
	# if request.method=="POST":
	# 	print(request.POST)
	next_url = None
	next_ = request.GET.get('next')
	if is_safe_url(next_, request.get_host()):
		next_url = next_
	return render(request,'billing/payment-method.html',{"publish_key":STRIPE_PUB_KEY, "next_url":next_url})


def payment_method_createview(request):
	if request.method=="POST" and request.is_ajax():
		print(request.POST)
		return JsonResponse({"message":"Success! Your card was added."})
	return HttpResponse("error", status=401)


