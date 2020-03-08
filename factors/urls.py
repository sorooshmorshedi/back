from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from factors.views.firstPeriodInventoryViews import FirstPeriodInventoryView
from factors.views.transferViews import TransferModelView, getTransferByPosition
from factors.views.factorViews import *

router = DefaultRouter()
router.register(r'expenses', ExpenseModelView, base_name='expense')
router.register(r'factors', FactorModelView, base_name='factor')
router.register(r'transfers', TransferModelView, base_name='transfer')

urlpatterns = router.urls + [
    url(r'^getFactorByPosition$', getFactorByPosition, name=''),
    url(r'^notPaidFactors$', getNotPaidFactors, name=''),
    url(r'^factors/newCodes$', newCodesForFactor, name=''),
    url(r'^factors/definite/(?P<pk>[0-9]+)$', DefiniteFactor.as_view(), name=''),

    url(r'^getTransferByPosition$', getTransferByPosition, name=''),

    url(r'^firstPeriodInventory$', FirstPeriodInventoryView.as_view(), name=''),
]
