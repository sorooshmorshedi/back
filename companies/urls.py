from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('financialYears', FinancialYearModelView)
router.register('', CompanyModelView)

urlpatterns = router.urls

urlpatterns += [
    url(r'^closeAccounts$', CloseAccountsView.as_view()),
]

