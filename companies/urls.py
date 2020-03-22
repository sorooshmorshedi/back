from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from companies.views.financialYear import CloseFinancialYearView, MoveFinancialYearView
from companies.views.companies import CompanyModelView
from companies.views.companies import FinancialYearModelView


router = DefaultRouter()
router.register('financialYears', FinancialYearModelView, base_name='financial-year')
router.register('', CompanyModelView, base_name='company')

urlpatterns = router.urls

urlpatterns += [
    url(r'^closeFinancialYear$', CloseFinancialYearView.as_view()),
    url(r'^moveFinancialYear$', MoveFinancialYearView.as_view()),
]

