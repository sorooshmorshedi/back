from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from sanads.sanads.views import SanadListCreate, SanadDetail, newCodeForSanad, getSanadByCode, ReorderSanadsApiView
from sanads.transactions.views import TransactionListCreate, TransactionDetail, newCodeForTransaction, \
    getTransactionByCode

router = DefaultRouter()

urlpatterns = router.urls + [

    url(r'^sanads$', SanadListCreate.as_view(), name=''),
    url(r'^sanads/(?P<pk>[0-9]+)$', SanadDetail.as_view(), name=''),
    url(r'^sanads/newCode$', newCodeForSanad, name=''),
    url(r'^sanads/getSanadByCode$', getSanadByCode, name=''),
    url(r'^sanads/reorder$', ReorderSanadsApiView.as_view(), name=''),

    url(r'^transactions$', TransactionListCreate.as_view(), name=''),
    url(r'^transactions/(?P<pk>[0-9]+)$', TransactionDetail.as_view(), name=''),
    url(r'^transactions/newCodes$', newCodeForTransaction, name=''),
    url(r'^transactions/getTransactionByCode$', getTransactionByCode, name=''),
]
