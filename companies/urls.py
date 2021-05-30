from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from companies.views.company_users_views import CompanyUserInvitationModelView, CompanyUserModelView
from companies.views.financialYearViews import CloseFinancialYearView, MoveFinancialYearView, \
    CancelFinancialYearClosingView, FinancialYearModelView
from companies.views.companyViews import CompanyModelView, CompanyListView

router = DefaultRouter()
router.register('financialYears', FinancialYearModelView, basename='financial-year')
router.register('companyUserInvitations', CompanyUserInvitationModelView, basename='company-user-invitation')
router.register('companyUsers', CompanyUserModelView, basename='company-user')
router.register('', CompanyModelView, basename='company')

urlpatterns = router.urls

urlpatterns += [
    url('list', CompanyListView.as_view()),

    url(r'^closeFinancialYear$', CloseFinancialYearView.as_view()),
    url(r'^cancelFinancialYearClosing$', CancelFinancialYearClosingView.as_view()),
    url(r'^moveFinancialYear$', MoveFinancialYearView.as_view()),
]
