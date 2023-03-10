from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from cheques.views import ChequebookModelView, ChequeApiView, \
    ChangeChequeStatus, DeleteStatusChangeView, \
    SubmitChequeApiView, RevertChequeInFlowStatusView, ChequeByPositionApiView, ConfirmCheque, RevokeBlankPaidChequeView, ChequeMetaView

router = DefaultRouter()
router.register(r'chequebooks', ChequebookModelView, basename='chequebooks')

urlpatterns = router.urls + [
    url(r'^cheques/(?P<pk>[0-9]+)$', ChequeApiView.as_view(), name='chequeDetail'),
    url(r'^cheques/submit', SubmitChequeApiView.as_view(), name='submitCheque'),
    url(r'^getChequeByPosition$', ChequeByPositionApiView.as_view(), name='getChequeByPosition'),
    url(r'^cheques/(?P<pk>[0-9]+)/confirm$', ConfirmCheque.as_view(), name=''),
    url(r'^cheques/meta$', ChequeMetaView.as_view(), name=''),

    # cheque id
    url(r'^cheques/changeStatus/(?P<pk>[0-9]+)$', ChangeChequeStatus.as_view(), name='changeChequeStatus'),
    # statusChange id
    url(r'^statusChange/(?P<pk>[0-9]+)/$', DeleteStatusChangeView.as_view(), name='ChequeStatusView'),
    url(r'^cheques/revertInFlowStatus/(?P<pk>[0-9]+)$', RevertChequeInFlowStatusView.as_view(),
        name='revertChequeInFlowStatus'),

    # url(r'^getChequebookByPosition$', ChequebookByPositionApiView.as_view(), name='getChequebookByPosition'),

    url('changeStatus/revokeBlankPaidCheque/', RevokeBlankPaidChequeView.as_view()),
]
