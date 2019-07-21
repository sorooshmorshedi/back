from django.conf.urls import url

from accounts.accounts.views import FloatAccountListCreate, FloatAccountDetail, FloatAccountGroupListCreate, \
    FloatAccountGroupDetail, AccountTypeList, AccountListCreate, AccountDetail, getAccountRemain, \
    IndependentAccountListCreate, IndependentAccountDetail, PersonListCreate, PersonDetail, BankListCreate, BankDetail
from accounts.costCenters.views import CostCenterListCreate, CostCenterDetail, CostCenterGroupListCreate, \
    CostCenterGroupDetail
from accounts.defaultAccounts.views import DefaultAccountListCreate, DefaultAccountDetail


urlpatterns = [
    url(r'^costCenters$', CostCenterListCreate.as_view(), name='costCenters'),
    url(r'^costCenters/(?P<pk>[0-9]+)$', CostCenterDetail.as_view(), name='costCenterDetail'),
    url(r'^costCenterGroups$', CostCenterGroupListCreate.as_view(), name='costCenterGroups'),
    url(r'^costCenterGroups/(?P<pk>[0-9]+)$', CostCenterGroupDetail.as_view(), name='costCenterGroupDetail'),

    url(r'^floatAccounts$', FloatAccountListCreate.as_view(), name='floatAccounts'),
    url(r'^floatAccounts/(?P<pk>[0-9]+)$', FloatAccountDetail.as_view(), name='floatAccountDetail'),
    url(r'^floatAccountGroups$', FloatAccountGroupListCreate.as_view(), name='floatAccountGroups'),
    url(r'^floatAccountGroups/(?P<pk>[0-9]+)$', FloatAccountGroupDetail.as_view(), name='floatAccountGroupDetail'),

    # ChangeIt to list
    url(r'^accountTypes$', AccountTypeList.as_view(), name='accountTypes'),

    url(r'^accounts$', AccountListCreate.as_view(), name='Accounts'),
    url(r'^accounts/(?P<pk>[0-9]+)$', AccountDetail.as_view(), name='AccountDetail'),
    url(r'^accounts/(?P<pk>[0-9]+)/remain$', getAccountRemain, name='AccountRemain'),

    url(r'^independentAccounts$', IndependentAccountListCreate.as_view(), name='Accounts'),
    url(r'^independentAccounts/(?P<pk>[0-9]+)$', IndependentAccountDetail.as_view(), name='AccountDetail'),

    url(r'^persons$', PersonListCreate.as_view()),
    url(r'^persons/(?P<pk>[0-9]+)$', PersonDetail.as_view()),

    url(r'^banks$', BankListCreate.as_view()),
    url(r'^banks/(?P<pk>[0-9]+)$', BankDetail.as_view()),

    url(r'^defaultAccounts$', DefaultAccountListCreate.as_view(), name=''),
    url(r'^defaultAccounts/(?P<pk>[0-9]+)$', DefaultAccountDetail.as_view(), name=''),
]
