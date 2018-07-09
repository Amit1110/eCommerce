
from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

class SearchProductView(ListView):
	#queryset = Product.objects.all()
	template_name = "search/view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(SearchProductView, self).get_context_data(*args, **kwargs)
		query = self.request.GET.get('q')
		context['query'] = query
		#SearchQuery.objects.create(query=query)
		return context
	
	def get_queryset(self,*args,**kwargs):
		request = self.request
		print(request.GET)
		query = request.GET.get('q',None)
		if query is not None:
			
			return Product.objects.search(query)
		else:
			return Product.objects.feature()		
		'''
		__icontains = field contains it
		__exact = field is equal to it
		'''
