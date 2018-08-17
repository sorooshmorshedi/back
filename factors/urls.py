from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'factorExpenses', FactorExpenseModelView)
router.register(r'factors', FactorModelView)

urlpatterns = router.urls + [
    url(r'^factorItems/mass$', FactorItemMass.as_view(), name=''),
]
