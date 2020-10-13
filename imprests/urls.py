from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from imprests.views import ImprestSettlementModelView, ImprestSettlementByPositionView, ConfirmImprest

router = DefaultRouter()
router.register('imprestSettlement', ImprestSettlementModelView, base_name='imprestSettlement')

urlpatterns = router.urls

urlpatterns += [
    url(r'^imprestSettlement/byPosition$', ImprestSettlementByPositionView.as_view()),
    url(r'^imprestSettlement/(?P<pk>[0-9]+)/confirm/$', ConfirmImprest.as_view(), name=''),
]
