from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'expenses', ExpenseModelView)
router.register(r'factors', FactorModelView)
router.register(r'receipts', ReceiptModelView)

urlpatterns = router.urls + [
    url(r'^items/mass$', FactorItemMass.as_view(), name=''),
    url(r'^getFactorByCode$', getFactorByCode, name=''),
    url(r'^factorExpenses/mass$', FactorExpenseMass.as_view(), name=''),
    url(r'^factors/updateSanadAndReceipt/(?P<pk>[0-9]+)$', FactorSanadAndReceiptUpdate.as_view(), name=''),
    url(r'^notPaidFactors$', getNotPaidFactors, name=''),
    url(r'^factors/newCodes$', newCodesForFactor, name=''),
    url(r'^factorPayments/mass$', FactorPaymentMass.as_view(), name=''),

    url(r'^receiptItems/mass$', ReceiptItemMass.as_view(), name=''),
    url(r'^receipts/newCodes$', newCodesForReceipt, name=''),

    url(r'^firstPeriodInventory$', FirstPeriodInventoryView.as_view(), name=''),
]
