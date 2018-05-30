from django.conf.urls import url, include
from django.urls import path

from .views import *


urlpatterns = [
    url(r'^$', CompanyListCreate.as_view(), name='companies'),
    url(r'^(?P<pk>[0-9]+)', CompanyDetail.as_view(), name='companyDetail'),
]
