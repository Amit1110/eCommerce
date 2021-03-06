from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,get_user_model
from .forms import ContactForm,LoginForm,RegisterForm

def home_page(request):
	#print(request.session.get("first_name", "Unknown")) #sec value default
	context ={
	"title":"Hello World",
	'content': 'Welcome to page',
	'premium_content':'YEAHHHH'
	}
	return render(request,'home_page.html',context)

def about_page(request):
	context = {
	"title":"About"
	}
	return render(request,'home_page.html',context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
	"title":"Contact",
	"form":contact_form
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
		if request.is_ajax():
			return JsonResponse({"message":"Thank You!! For your submission"})

	if contact_form.errors:
		errors = contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors,status=400, content_type='application/json')
	#if request.method=="POST":
	#	print(request.POST)	
	return render(request,'contact/view.html',context)



	