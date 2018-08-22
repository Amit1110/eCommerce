from django.shortcuts import render

STRIPE_PUB_KEY = "pk_test_ThzzgkBGhdMHqFaMi093UcFe"

def payment_method_view(request):
	if request.method=="POST":
		print(request.POST)
	return render(request,'billing/payment-method.html',{"publish_key":STRIPE_PUB_KEY})


