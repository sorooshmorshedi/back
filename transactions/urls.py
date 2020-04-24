from django.conf.urls import url
from transactions.views import TransactionCreateView, TransactionDetail, newCodeForTransaction, GetTransactionByCodeView

urlpatterns = [
    url(r'^$', TransactionCreateView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)$', TransactionDetail.as_view(), name=''),
    url(r'^newCodes$', newCodeForTransaction, name=''),
    url(r'^getTransactionByCode$', GetTransactionByCodeView.as_view(), name=''),
]
