from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from imprests.views import ImprestSettlementModelView, ImprestSettlementByPositionView, GetAccountNotSettledImprestsView

router = DefaultRouter()
router.register('imprestSettlement', ImprestSettlementModelView, base_name='imprestSettlement')

urlpatterns = router.urls

urlpatterns += [
    url(r'^imprestSettlement/byPosition$', ImprestSettlementByPositionView.as_view()),
    url(r'^notSettledImprests$', GetAccountNotSettledImprestsView.as_view()),
]
