from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from products.views import (ProductListView, productlistview,ProductDetailView, productdetailview,
    ProductFeaturedListView,ProductFeaturedDetailView,ProductDetailSlugView)

from .views import home_page,contact_page,about_page,login_page,register_page

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page),
    url(r'^about/$', about_page),
    url(r'^contact/$', contact_page),
    url(r'^login/$', login_page),
    url(r'^register/$', register_page),
    url(r'^product-fbv/$', productlistview),
    url(r'^featured/$', ProductFeaturedListView.as_view()),
    url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
    url(r'^products/$', ProductListView.as_view()),
    url(r'^product-fbv/(?P<pk>\d+)/$', productdetailview),
    #url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
    url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#superuser
#admin
#admin@admin.com
#asdf1234