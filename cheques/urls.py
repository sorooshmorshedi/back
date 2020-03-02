from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from cheques.views import ChequebookModelView, ChequeByPositionApiView, ChequeApiView, \
    ChangeChequeStatus, revertChequeInFlowStatus, StatusChangeView, ChequebookByPositionApiView, SubmitChequeApiView

router = DefaultRouter()
router.register(r'chequebooks', ChequebookModelView, base_name='chequebooks')

urlpatterns = router.urls + [
    url(r'^cheques/(?P<pk>[0-9]+)$', ChequeApiView.as_view(), name='changeChequeStatus'),
    url(r'^cheques/submit', SubmitChequeApiView.as_view(), name='submitCheque'),
    url(r'^getChequeByPosition$', ChequeByPositionApiView.as_view(), name='getChequeByPosition'),

    # cheque id
    url(r'^cheques/changeStatus/(?P<pk>[0-9]+)$', ChangeChequeStatus.as_view(), name='changeChequeStatus'),
    # statusChange id
    url(r'^statusChange/(?P<pk>[0-9]+)/$', StatusChangeView.as_view(), name='ChequeStatusView'),
    url(r'^cheques/revertInFlowStatus/(?P<pk>[0-9]+)$', revertChequeInFlowStatus, name='revertChequeInFlowStatus'),

    url(r'^getChequebookByPosition$', ChequebookByPositionApiView.as_view(), name='getChequebookByPosition'),
]
