from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from companies.views.financialYear import CloseAccountsView
from companies.views.companies import CompanyModelView
from companies.views.companies import FinancialYearModelView


router = DefaultRouter()
router.register('financialYears', FinancialYearModelView)
router.register('', CompanyModelView)

urlpatterns = router.urls

urlpatterns += [
    url(r'^closeAccounts$', CloseAccountsView.as_view()),
]

