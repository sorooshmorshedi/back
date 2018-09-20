from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from sanads.sanads.views import *
from sanads.transactions.views import *
from .views import *

router = DefaultRouter()
router.register(r'sanadItems', SanadItemListCreate)
router.register(r'transactionItems', TransactionItemModelView)

urlpatterns = router.urls + [


    url(r'^sanads$', SanadListCreate.as_view(), name=''),
    url(r'^sanads/(?P<pk>[0-9]+)$', SanadDetail.as_view(), name=''),
    url(r'^sanads/newCode$', newCodeForSanad, name=''),

    url(r'^sanadItems/mass$', SanadItemMass.as_view(), name=''),

    url(r'^transactions$', TransactionListCreate.as_view(), name=''),
    url(r'^transactions/(?P<pk>[0-9]+)$', TransactionDetail.as_view(), name=''),
    url(r'^transactions/newCode$', newCodeForTransaction, name=''),
    url(r'^transactionItems/mass$', TransactionItemMass.as_view(), name=''),
]
