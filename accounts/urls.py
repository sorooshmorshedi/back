from django.conf.urls import url

from accounts.accounts.views import FloatAccountListCreate, FloatAccountDetail, FloatAccountGroupListCreate, \
    FloatAccountGroupDetail, AccountTypeList, AccountListCreate, AccountDetail, getAccountRemain
from accounts.defaultAccounts.views import DefaultAccountListCreate, DefaultAccountDetail

urlpatterns = [
    url(r'^floatAccounts$', FloatAccountListCreate.as_view(), name='floatAccounts'),
    url(r'^floatAccounts/(?P<pk>[0-9]+)$', FloatAccountDetail.as_view(), name='floatAccountDetail'),
    url(r'^floatAccountGroups$', FloatAccountGroupListCreate.as_view(), name='floatAccountGroups'),
    url(r'^floatAccountGroups/(?P<pk>[0-9]+)$', FloatAccountGroupDetail.as_view(), name='floatAccountGroupDetail'),

    # ChangeIt to list
    url(r'^accountTypes$', AccountTypeList.as_view(), name='accountTypes'),

    url(r'^accounts$', AccountListCreate.as_view(), name='accounts'),
    url(r'^accounts/(?P<pk>[0-9]+)$', AccountDetail.as_view(), name='accountDetail'),
    url(r'^accounts/(?P<pk>[0-9]+)/remain$', getAccountRemain, name='accountRemain'),

    url(r'^defaultAccounts$', DefaultAccountListCreate.as_view(), name=''),
    url(r'^defaultAccounts/(?P<pk>[0-9]+)$', DefaultAccountDetail.as_view(), name=''),
]
