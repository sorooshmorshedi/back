from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from cheques.views import *

router = DefaultRouter()
router.register(r'cheques', ChequeModelView)
router.register(r'chequebooks', ChequebookModelView)

urlpatterns = router.urls + [
    # cheque id
    url(r'^cheques/changeStatus/(?P<pk>[0-9]+)$', ChangeChequeStatus.as_view(), name='changeChequeStatus'),
    url(r'^cheques/revertInFlowStatus/(?P<pk>[0-9]+)$', revertChequeInFlowStatus, name='revertChequeInFlowStatus'),
    # statusChange id
    url(r'^statusChange/(?P<pk>[0-9]+)$', StatusChangeView.as_view(), name='ChequeStatusView'),
]
