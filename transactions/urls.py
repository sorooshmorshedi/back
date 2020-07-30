from django.conf.urls import url
from transactions.views import TransactionCreateView, TransactionDetail, TransactionByPositionView, ConfirmTransaction

urlpatterns = [
    url(r'^$', TransactionCreateView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)$', TransactionDetail.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/confirm/$', ConfirmTransaction.as_view(), name=''),
    url(r'^byPosition$', TransactionByPositionView.as_view(), name=''),
]
