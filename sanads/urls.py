from django.conf.urls import url, include
from django.urls import path

from .views import *


urlpatterns = [

    url(r'^RPTypes$', RPTypeListCreate.as_view(), name='companies'),
    url(r'^RPTypes/(?P<pk>[0-9]+)$', RPTypeDetail.as_view(), name='companyDetail'),
]
