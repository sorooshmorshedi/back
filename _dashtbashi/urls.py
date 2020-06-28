from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from _dashtbashi.views import DriverModelView, CarModelView, DrivingModelView, AssociationCommissionModelView, \
    RemittanceModelView, RemittanceByPositionView, LadingModelView, LadingByPositionView, RemittanceByCodeView

router = DefaultRouter()
router.register('drivers', DriverModelView, base_name='drivers')
router.register('cars', CarModelView, base_name='cars')
router.register('drivings', DrivingModelView, base_name='drivings')
router.register('associationCommissions', AssociationCommissionModelView, base_name='associationCommissions')

router.register('remittances', RemittanceModelView, base_name='remittances')
router.register('ladings', LadingModelView, base_name='ladings')

urlpatterns = router.urls

urlpatterns += [
    url(r'^remittances/byPosition$', RemittanceByPositionView.as_view()),
    url(r'^remittances/byCode$', RemittanceByCodeView.as_view()),

    url(r'^ladings/byPosition$', LadingByPositionView.as_view()),
]
