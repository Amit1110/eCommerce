from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.http import Http404
from .models import Product

from .models import Product

from carts.models import Cart


class ProductFeaturedListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self,*args,**kwargs):
		request = self.request
		return Product.objects.feature()


class ProductFeaturedDetailView(DetailView):
	#queryset = Product.objects.all()
	template_name = "products/featured-detail.html"

	
	def get_queryset(self,*args,**kwargs):
		request = self.request
		return Product.objects.feature()


class ProductListView(ListView):
	#queryset = Product.objects.all()
	template_name = "products/list.html"

	# def get_context_data(self,*args,**kwargs):
	# 	context = super(ProductListView,self).get_context_data(*args,**kwargs)
	# 	print(context)
	# 	return context

	def get_context_data(self,*args,**kwargs):
		context = super(ProductListView,self).get_context_data(*args,**kwargs)
		print(context)
		return context

	def get_queryset(self,*args,**kwargs):
		request = self.request
		return Product.objects.all()

def productlistview(request):
	queryset = Product.objects.all()
	context = {
		'object_list' : queryset
	}
	return render(request,"products/list.html",context)
		
class ProductDetailView(DetailView):
	#queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_context_data(self,*args,**kwargs):
		context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
		print(context)
		return context

	def get_object(self,*args,**kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product does not exist")
		return instance
	# def get_queryset(self,*args,**kwargs):
	# 	request = self.request
	# 	pk = self.kwargs.get('pk')
	# 	return Product.objects.filter(pk=pk)


def productdetailview(request,pk = None,*args,**kwargs):
	#instance = Product.objects.get(pk=pk)
	#instance = get_object_or_404(Product,pk=pk)
	'''
	try:
		instance = Product.objects.get(id=pk)
	except Product.DoesNotExist:
	    print('no product here')
	    raise Http404("Product does not exist")
	except:
	    print("nothing")
	'''
	instance = Product.objects.get_by_id(pk)
	if instance is None:
		raise Http404("Product does not exist")

	'''
	qs = Product.objects.filter(id=pk)
	print(qs)
	if qs.exists() and qs.count() == 1:
		instance = qs.first()
	else:
		raise Http404("Product does not exist")
	'''
	context = {
		'object' : instance
	}
	return render(request,"products/detail.html",context)


class ProductDetailSlugView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_context_data(self,*args, **kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
		request  = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj
		return context

	def get_object(self,*args,**kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		#instance = get_object_or_404(Product,slug = slug)
		try:
			instance = Product.objects.get(slug = slug)
		except Product.DoesNotExist:
			raise Http404("Not found..")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug)
			instance = qs.first()
		except:
			raise Http404("Uhhhhmmm")

		return instance