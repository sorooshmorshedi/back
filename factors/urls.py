from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from factors.views.factorViews import ExpenseModelView, FactorModelView, NotPaidFactorsView, newCodesForFactor, \
    DefiniteFactor, GetFactorByPositionView
from factors.views.firstPeriodInventoryViews import FirstPeriodInventoryView
from factors.views.transferViews import TransferModelView, GetTransferByPositionView

router = DefaultRouter()
router.register(r'expenses', ExpenseModelView, base_name='expense')
router.register(r'factors', FactorModelView, base_name='factor')
router.register(r'transfers', TransferModelView, base_name='transfer')

urlpatterns = router.urls + [
    url(r'^getFactorByPosition$', GetFactorByPositionView.as_view(), name=''),
    url(r'^notPaidFactors$', NotPaidFactorsView.as_view(), name=''),
    url(r'^factors/newCodes$', newCodesForFactor, name=''),
    url(r'^factors/definite/(?P<pk>[0-9]+)$', DefiniteFactor.as_view(), name=''),

    url(r'^getTransferByPosition$', GetTransferByPositionView.as_view(), name=''),

    url(r'^firstPeriodInventory$', FirstPeriodInventoryView.as_view(), name=''),
]
