from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from reports.balance.views import accountBalanceView, floatAccountBalanceView
from reports.balanceSheet.views import balanceSheetView
from reports.bill.views import BillListView
from reports.incomeStatement.views import incomeStatementView
from reports.inventory.views import InventoryListView
from reports.journal.views import JournalListView
from reports.ledger.views import LedgerListView
from reports.lists.export_views import SanadExportView, FactorExportView, TransactionExportView
from reports.lists.views import *
from reports.views import exportTest, ExportVerifiersModelView

# Lists
urlpatterns = [
    url(r'^lists/transactions$', TransactionListView.as_view(), name=''),
    url(r'^lists/cheques$', ChequeListView.as_view(), name=''),
    url(r'^lists/chequebooks$', ChequebookListView.as_view(), name=''),
    url(r'^lists/sanads$', SanadListView.as_view(), name=''),
    url(r'^lists/sanads/unbalanced$', UnbalancedSanadListView.as_view(), name=''),
    url(r'^lists/sanads/empty$', EmptySanadListView.as_view(), name=''),
    url(r'^lists/factors$', FactorListView.as_view(), name=''),
    url(r'^lists/factorItems$', FactorItemListView.as_view(), name=''),
]

# Lists Export
urlpatterns += [
    url(r'^lists/sanads/(?P<export_type>\S+)', SanadExportView.as_view(), name=''),
    url(r'^lists/factors/(?P<export_type>\S+)', FactorExportView.as_view(), name=''),
    url(r'^lists/transactions/(?P<export_type>\S+)', TransactionExportView.as_view(), name=''),
]

# Reports
urlpatterns += [
    url(r'^balance$', accountBalanceView, name=''),
    url(r'^balance/floats$', floatAccountBalanceView, name=''),
    url(r'^ledger$', LedgerListView.as_view(), name=''),
    url(r'^bill$', BillListView.as_view(), name=''),
    url(r'^journal$', JournalListView.as_view(), name=''),
    url(r'^export$', exportTest, name=''),
    url(r'^incomeStatement$', incomeStatementView, name=''),
    url(r'^balanceSheet$', balanceSheetView, name=''),
    url(r'^inventory$', InventoryListView.as_view(), name=''),
]


# Other
router = DefaultRouter()
router.register('exportVerifiers', ExportVerifiersModelView, base_name='export-verifiersgt')
urlpatterns += router.urls
