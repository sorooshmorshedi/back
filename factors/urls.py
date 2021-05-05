from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from factors.views.adjustment_views import AdjustmentModelView, GetAdjustmentByPositionView
from factors.views.factorViews import ExpenseModelView, FactorModelView, GetFactorByPositionView, \
    ConfirmFactor
from factors.views.definite_factor import DefiniteFactor
from factors.views.firstPeriodInventoryViews import FirstPeriodInventoryView
from factors.views.transferViews import TransferModelView, GetTransferByPositionView
from factors.views.warehouse_handling_view import WarehouseHandlingModelView, GetWarehouseHandlingByPositionView, \
    WarehouseHandlingDefiniteView

router = DefaultRouter()
router.register(r'expenses', ExpenseModelView, basename='expense')
router.register(r'factors', FactorModelView, basename='factor')
router.register(r'transfers', TransferModelView, basename='transfer')
router.register(r'adjustments', AdjustmentModelView, basename='adjustment')
router.register(r'warehouseHandlings', WarehouseHandlingModelView, basename='warehouseHandling')

urlpatterns = router.urls + [
    url(r'^factors/byPosition$', GetFactorByPositionView.as_view(), name=''),
    url(r'^factors/(?P<pk>[0-9]+)/confirm/$', ConfirmFactor.as_view(), name=''),
    url(r'^factors/definite/(?P<pk>[0-9]+)$', DefiniteFactor.as_view(), name=''),

    url(r'^transfers/byPosition$', GetTransferByPositionView.as_view(), name=''),

    url(r'^adjustments/byPosition$', GetAdjustmentByPositionView.as_view(), name=''),

    url(r'^warehouseHandlings/byPosition$', GetWarehouseHandlingByPositionView.as_view(), name=''),
    url(r'^warehouseHandlings/definite$', WarehouseHandlingDefiniteView.as_view(), name=''),

    url(r'^firstPeriodInventory$', FirstPeriodInventoryView.as_view(), name=''),
]
