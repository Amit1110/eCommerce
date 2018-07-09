from django.conf.urls import url

from .views import (SearchProductView)


urlpatterns = [
    url(r'^$', SearchProductView.as_view(),name='query'),
]


#superuser
#admin
#admin@admin.com
#asdf1234