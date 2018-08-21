from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'expenses', ExpenseModelView)
router.register(r'factors', FactorModelView)

urlpatterns = router.urls + [
    url(r'^items/mass$', FactorItemMass.as_view(), name=''),
    url(r'^factorExpenses/mass$', FactorExpenseMass.as_view(), name=''),
]
