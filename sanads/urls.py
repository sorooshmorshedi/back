from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from sanads.sanads.views import *
from sanads.transactions.views import *
from .views import *

router = DefaultRouter()
router.register(r'sanadItems', SanadItemListCreate)
router.register(r'transactionItems', TransactionItemListCreate)

urlpatterns = router.urls + [

    url(r'^RPTypes$', RPTypeListCreate.as_view(), name='companies'),
    url(r'^RPTypes/(?P<pk>[0-9]+)$', RPTypeDetail.as_view(), name='companyDetail'),

    url(r'^sanads$', SanadListCreate.as_view(), name='companies'),
    url(r'^sanads/(?P<pk>[0-9]+)$', SanadDetail.as_view(), name='companyDetail'),

    url(r'^transactions$', TransactionListCreate.as_view(), name='companies'),
    url(r'^transactions/(?P<pk>[0-9]+)$', TransactionDetail.as_view(), name='companyDetail'),
]
