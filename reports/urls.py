from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from reports.balance.views import FloatAccountBalanceByGroupView, FloatAccountBalanceView, \
    FloatAccountBalanceByGroupExportView, FloatAccountBalanceExportView
from reports.balance.account_balance import AccountBalanceView, AccountBalanceExportView
from reports.balanceSheet.views import BalanceSheetView, BalanceSheetExportView
from reports.buySale.views import BuySaleReportView, BuySaleReportExportView
from reports.incomeStatement.views import IncomeStatementView, IncomeStatementExportView
from reports.inventory.views import WareInventoryListView, AllWaresInventoryListView, WarehouseInventoryListView, \
    AllWarehousesInventoryListView, WareInventoryExportView, AllWaresInventoryExportView,\
    WarehouseInventoryExportView, AllWarehousesInventoryExportView
from reports.sanadItems.views import SanadItemReportView, SanadItemReportExportView
from reports.lists.export_views import SanadExportView, FactorExportView, TransactionExportView, TransferExportView, \
    AdjustmentExportView, WarehouseHandlingExportView, ImprestSettlementExportView, TenderExportView, \
    ContractExportview, StatementExportView, SupplementExportView, ContractDetailExportview

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
    url(r'^lists/factorsAggregatedSanads$', FactorsAggregatedSanadListView.as_view(), name=''),
    url(r'^lists/transfers$', TransferListView.as_view(), name=''),
    url(r'^lists/factorItems$', FactorItemListView.as_view(), name=''),
    url(r'^lists/adjustments$', AdjustmentListView.as_view(), name=''),
    url(r'^lists/warehouseHandlings$', WarehouseHandlingListView.as_view(), name=''),
    url(r'^lists/salePrices$', SalePriceListView.as_view(), name=''),
    url(r'^lists/salePriceChanges$', SalePriceChangeListView.as_view(), name=''),
    url(r'^lists/wareSalePriceChanges$', WareSalePriceChangeListView.as_view(), name=''),
]

# Lists Export
urlpatterns += [
    url(r'^lists/sanads/(?P<export_type>\S+)', SanadExportView.as_view(), name=''),
    url(r'^lists/factors/(?P<export_type>\S+)', FactorExportView.as_view(), name=''),
    url(r'^lists/transfers/(?P<export_type>\S+)', TransferExportView.as_view(), name=''),
    url(r'^lists/transactions/(?P<export_type>\S+)', TransactionExportView.as_view(), name=''),
    url(r'^lists/adjustments/(?P<export_type>\S+)', AdjustmentExportView.as_view(), name=''),
    url(r'^lists/warehouseHandlings/(?P<export_type>\S+)', WarehouseHandlingExportView.as_view(), name=''),
    url(r'^lists/imprestSettlements/(?P<export_type>\S+)', ImprestSettlementExportView.as_view(), name=''),

    url(r'^tender/all/(?P<export_type>\S+)', TenderExportView.as_view(), name=''),
    url(r'^contract/all/(?P<export_type>\S+)', ContractExportview.as_view(), name=''),
    url(r'^statement/all/(?P<export_type>\S+)', StatementExportView.as_view(), name=''),
    url(r'^supplement/all/(?P<export_type>\S+)', SupplementExportView.as_view(), name=''),
    url(r'^contract/(?P<pk>\S+)/(?P<export_type>\S+)', ContractDetailExportview.as_view(), name=''),

]

# Reports
urlpatterns += [
    url(r'^balance$', AccountBalanceView.as_view(), name=''),
    url(r'^balance/floatsByGroup$', FloatAccountBalanceByGroupView.as_view(), name=''),
    url(r'^balance/floats$', FloatAccountBalanceView.as_view(), name=''),

    url(r'^balance/floats/(?P<export_type>\S+)', FloatAccountBalanceExportView.as_view(), name=''),
    url(r'^balance/floatsByGroup/(?P<export_type>\S+)', FloatAccountBalanceByGroupExportView.as_view(), name=''),
    url(r'^balance/(?P<export_type>\S+)', AccountBalanceExportView.as_view(), name=''),

    url(r'^sanadItems$', SanadItemReportView.as_view(), name=''),
    url(r'^sanadItems/(?P<export_type>\S+)', SanadItemReportExportView.as_view(), name=''),

    url(r'^export$', exportTest, name=''),

    url(r'^incomeStatement$', IncomeStatementView.as_view(), name=''),
    url(r'^incomeStatement/(?P<export_type>\S+)$', IncomeStatementExportView.as_view(), name=''),

    url(r'^balanceSheet$', BalanceSheetView.as_view(), name=''),
    url(r'^balanceSheet/(?P<export_type>\S+)$', BalanceSheetExportView.as_view(), name=''),

    url(r'^buySale$', BuySaleReportView.as_view(), name=''),
    url(r'^buySale/(?P<export_type>\S+)', BuySaleReportExportView.as_view(), name=''),

    url(r'^inventory/ware$', WareInventoryListView.as_view(), name=''),
    url(r'^inventory/ware/all$', AllWaresInventoryListView.as_view(), name=''),
    url(r'^inventory/warehouse$', WarehouseInventoryListView.as_view(), name=''),
    url(r'^inventory/warehouse/all$', AllWarehousesInventoryListView.as_view(), name=''),

    url(r'^inventory/ware/all/(?P<export_type>\S+)', AllWaresInventoryExportView.as_view(), name=''),
    url(r'^inventory/ware/(?P<export_type>\S+)', WareInventoryExportView.as_view(), name=''),

    url(r'^inventory/warehouse/all/(?P<export_type>\S+)', AllWarehousesInventoryExportView.as_view(), name=''),
    url(r'^inventory/warehouse/(?P<export_type>\S+)', WarehouseInventoryExportView.as_view(), name=''),

    url(r'^tender/all$', TenderListView.as_view(), name='tenderList'),
    url(r'^contract/all$', ContractListView.as_view(), name='contractList'),
    url(r'^statement/all$', StatementListView.as_view(), name='statementList'),
    url(r'^supplement/all$', SupplementListView.as_view(), name='supplementList'),

]

# Other
router = DefaultRouter()
router.register('exportVerifiers', ExportVerifiersModelView, basename='export-verifiers')
urlpatterns += router.urls
