from django.conf.urls import url
from transactions.views import TransactionCreateView, TransactionDetailView, TransactionByPositionView, \
    ConfirmTransaction, TransactionFactorsListView

urlpatterns = [
    url(r'^$', TransactionCreateView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/$', TransactionDetailView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/confirm/$', ConfirmTransaction.as_view(), name=''),
    url(r'^byPosition$', TransactionByPositionView.as_view(), name=''),
    url(r'^factors$', TransactionFactorsListView.as_view(), name=''),
]
