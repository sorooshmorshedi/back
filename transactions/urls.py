from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from transactions.views import TransactionCreateView, TransactionDetailView, TransactionByPositionView, \
    ConfirmTransaction, TransactionFactorsListView, QuickFactorTransaction, DefineTransactionView, \
    ToggleTransactionLockView, BankingOperationModelView


urlpatterns = [
    url(r'^$', TransactionCreateView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/$', TransactionDetailView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/confirm/$', ConfirmTransaction.as_view(), name=''),
    url(r'^byPosition$', TransactionByPositionView.as_view(), name=''),
    url(r'^factors$', TransactionFactorsListView.as_view(), name=''),
    url(r'^quickFactorTransaction$', QuickFactorTransaction.as_view(), name=''),
    url(r'^define/$', DefineTransactionView.as_view(), name=''),
    url(r'^toggleLock/$', ToggleTransactionLockView.as_view(), name=''),
]

router = DefaultRouter()
router.register('bankingOperations', BankingOperationModelView, basename='bankingOperations')

urlpatterns += router.urls
