from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from _dashtbashi.export_views import LadingReportExportView
from _dashtbashi.report_views import RemittanceReportView, OtherDriverPaymentReport, LadingBillSeriesListView, \
    LadingsReportView, OilCompanyLadingReportView, OilCompanyLadingItemReportView
from _dashtbashi.views import DriverModelView, CarModelView, DrivingModelView, AssociationModelView, \
    RemittanceModelView, RemittanceByPositionView, LadingModelView, LadingByPositionView, RemittanceByCodeView, \
    LadingBillSeriesModelView, LadingBillSeriesByPositionView, RevokeLadingBillNumberView, OilCompanyLadingModelView, \
    OilCompanyLadingByPositionView, OtherDriverPaymentModelView, ConfirmRemittance, ConfirmLading, \
    ConfirmOilCompanyLading, ConfirmOtherDriverPayment, OtherDriverPaymentByPositionView, LadingBillNumberListView

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

    url(r'^ladingBillNumbers/revoke$', RevokeLadingBillNumberView.as_view()),
    url(r'^ladingBillNumbers$', LadingBillNumberListView.as_view()),

    url(r'^remittances/byPosition$', RemittanceByPositionView.as_view()),
    url(r'^remittances/byCode$', RemittanceByCodeView.as_view()),

    url(r'^ladings/byPosition$', LadingByPositionView.as_view()),

    url(r'^oilCompanyLadings/byPosition$', OilCompanyLadingByPositionView.as_view()),

    url(r'^otherDriverPayments/byPosition$', OtherDriverPaymentByPositionView.as_view()),

    url(r'^remittances/(?P<pk>[0-9]+)/confirm/$', ConfirmRemittance.as_view(), name=''),
    url(r'^ladings/(?P<pk>[0-9]+)/confirm/$', ConfirmLading.as_view(), name=''),
    url(r'^oilCompanyLadings/(?P<pk>[0-9]+)/confirm/$', ConfirmOilCompanyLading.as_view(), name=''),
    url(r'^otherDriverPayments/(?P<pk>[0-9]+)/confirm/$', ConfirmOtherDriverPayment.as_view(), name=''),

    url(r'^report/otherDriverPayments$', OtherDriverPaymentReport.as_view(), name=''),
    url(r'^report/remittances/$', RemittanceReportView.as_view()),
    url(r'^report/ladingBillSeriesList/$', LadingBillSeriesListView.as_view()),
    url(r'^report/ladings/$', LadingsReportView.as_view()),
    url(r'^report/oilCompanyLadings/$', OilCompanyLadingReportView.as_view()),
    url(r'^report/oilCompanyLadings/detailed$', OilCompanyLadingItemReportView.as_view()),

    url(r'^report/ladings/(?P<export_type>\S+)', LadingReportExportView.as_view(), name=''),

]
