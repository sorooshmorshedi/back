from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from _dashtbashi.views import DriverModelView, CarModelView, DrivingModelView, AssociationModelView, \
    RemittanceModelView, RemittanceByPositionView, LadingModelView, LadingByPositionView, RemittanceByCodeView, \
    LadingBillSeriesModelView, LadingBillSeriesByPositionView, RevokeLadingBillNumber, OilCompanyLadingModelView, \
    OilCompanyLadingByPositionView, OtherDriverPaymentModelView

router = DefaultRouter()
router.register('drivers', DriverModelView, base_name='drivers')
router.register('cars', CarModelView, base_name='cars')
router.register('drivings', DrivingModelView, base_name='drivings')
router.register('associations', AssociationModelView, base_name='associations')
router.register('ladingBillSeries', LadingBillSeriesModelView, base_name='ladingBillSeries')

router.register('remittances', RemittanceModelView, base_name='remittances')
router.register('ladings', LadingModelView, base_name='ladings')
router.register('oilCompanyLadings', OilCompanyLadingModelView, base_name='oilCompanyLadings')
router.register('otherDriverPayments', OtherDriverPaymentModelView, base_name='otherDriverPayments')

urlpatterns = router.urls

urlpatterns += [
    url(r'^ladingBillSeries/byPosition$', LadingBillSeriesByPositionView.as_view()),

    url(r'^ladingBillNumbers/revoke$', RevokeLadingBillNumber.as_view()),

    url(r'^remittances/byPosition$', RemittanceByPositionView.as_view()),
    url(r'^remittances/byCode$', RemittanceByCodeView.as_view()),

    url(r'^ladings/byPosition$', LadingByPositionView.as_view()),

    url(r'^oilCompanyLadings/byPosition$', OilCompanyLadingByPositionView.as_view()),

]
