from django.conf.urls import url

from reports.balance.views import accountBalanceView
from reports.incomeStatement.views import incomeStatementView
from reports.journal.views import JournalListView
from reports.ledger.views import LedgerListView
from reports.lists.views import *
from reports.views import exportTest


urlpatterns = [
    url(r'^lists/transactions$', TransactionListView.as_view(), name=''),
    url(r'^lists/cheques$', ChequeListView.as_view(), name=''),
    url(r'^lists/chequebooks$', ChequebookListView.as_view(), name=''),
    url(r'^lists/sanads$', SanadListView.as_view(), name=''),
    url(r'^lists/factors$', FactorListView.as_view(), name=''),
    url(r'^lists/receipts$', ReceiptListView.as_view(), name=''),

    url(r'^balance$', accountBalanceView, name=''),

    url(r'^ledger$', LedgerListView.as_view(), name=''),

    url(r'^journal$', JournalListView.as_view(), name=''),

    url(r'^export$', exportTest, name=''),

    url(r'^incomeStatement$', incomeStatementView, name=''),
]
