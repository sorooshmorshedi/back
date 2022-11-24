from django.conf.urls import url
from django.urls import path
from contracting.views import TenderDetail, TenderApiView, ConfirmedTenderView, ContractApiView, ContractDetail, \
    StatementApiView, \
    StatementDetail, SupplementApiView, SupplementDetail, ContractPreviousValue, ContractChange, \
    AddTransactionTenderView, \
    AddContractPaymentTransactionView, AddContractReceivedTransactionView, ToggleTenderLockView, \
    ToggleContractLockView, ToggleStatementLockView, ToggleSupplementLockView, DefineTenderView, DefineContractView, \
    DefineStatementView, DefineSupplementView

urlpatterns = [
    path('tender/', TenderApiView.as_view(), name='tenderApi'),
    path('tender/<int:pk>/', TenderDetail.as_view(), name='tenderDetail'),
    path('tender/confirmed/<int:pk>/', ConfirmedTenderView.as_view(), name='confirmedTenderView'),
    path('tender/transaction/<int:pk1>/<int:pk2>/', AddTransactionTenderView.as_view(),
         name='addTransactionTenderView'),
    url(r'^tender/toggleLock/$', ToggleTenderLockView.as_view(), name='toggleTenderLockView'),
    url(r'^tender/define/$', DefineTenderView.as_view(), name='defineTenderView'),
    path('contract/', ContractApiView.as_view(), name='contractApi'),
    path('contract/<int:pk>/', ContractDetail.as_view(), name='contractDetail'),
    path('contract/received/<int:pk1>/<int:pk2>/', AddContractReceivedTransactionView.as_view(),
         name='addContractReceivedTransactionView'),
    path('contract/payment/<int:pk1>/<int:pk2>/', AddContractPaymentTransactionView.as_view(),
         name='addContractPaymentTransactionView'),
    path('contract/change/<int:pk>/', ContractChange.as_view(), name='contractChange'),
    url(r'^contract/toggleLock/$', ToggleContractLockView.as_view(), name='toggleContractLockView'),
    url(r'^contract/define/$', DefineContractView.as_view(), name='defineContractView'),
    path('statement/', StatementApiView.as_view(), name='statement'),
    path('statement/<int:pk>/', StatementDetail.as_view(), name='statementDetail'),
    url(r'^statement/toggleLock/$', ToggleStatementLockView.as_view(), name='toggleStatementLockView'),
    url(r'^statement/define/$', DefineStatementView.as_view(), name='definesStatementView'),
    path('supplement/', SupplementApiView.as_view(), name='supplementApi'),
    path('supplement/<int:pk>/', SupplementDetail.as_view(), name='supplementDetail'),
    path('supplement/previous/<int:pk>/', ContractPreviousValue.as_view(), name='contractPreviousValue'),
    url(r'^supplement/toggleLock/$', ToggleSupplementLockView.as_view(), name='toggleSupplementLockView'),
    url(r'^supplement/define/$', DefineSupplementView.as_view(), name='definesSupplementView'),
]
