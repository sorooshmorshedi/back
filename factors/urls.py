from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'expenses', ExpenseModelView, base_name='expense')
router.register(r'factors', FactorModelView, base_name='factor')

urlpatterns = router.urls + [
    url(r'^items/mass$', FactorItemMass.as_view(), name=''),
    url(r'^getFactorByCode$', getFactorByCode, name=''),
    url(r'^factorExpenses/mass$', FactorExpenseMass.as_view(), name=''),
    url(r'^factors/updateSanadAndReceipt/(?P<pk>[0-9]+)$', FactorSanadUpdate.as_view(), name=''),
    url(r'^notPaidFactors$', getNotPaidFactors, name=''),
    url(r'^factors/newCodes$', newCodesForFactor, name=''),
    url(r'^factorPayments/mass$', FactorPaymentMass.as_view(), name=''),

    url(r'^firstPeriodInventory$', FirstPeriodInventoryView.as_view(), name=''),
]
