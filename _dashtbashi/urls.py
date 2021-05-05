from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from _dashtbashi.export_views import LadingListExportView, OtherDriverPaymentListExportView, \
    OtherDriverPaymentFormExportView, LadingBillSeriesListExportView, LadingBillNumberListExportView, \
    RemittanceListExportView, OilCompanyLadingListExportView, OilCompanyLadingItemListExportView, \
    OilCompanyLadingFormExportView
from _dashtbashi.report_views import RemittanceListView, OtherDriverPaymentReport, LadingBillSeriesListView, \
    LadingListView, OilCompanyLadingListView, OilCompanyLadingItemListView
from _dashtbashi.views import DriverModelView, CarModelView, DrivingModelView, AssociationModelView, \
    RemittanceModelView, RemittanceByPositionView, LadingModelView, LadingByPositionView, RemittanceByCodeView, \
    LadingBillSeriesModelView, LadingBillSeriesByPositionView, RevokeLadingBillNumberView, OilCompanyLadingModelView, \
    OilCompanyLadingByPositionView, OtherDriverPaymentModelView, ConfirmRemittance, ConfirmLading, \
    ConfirmOilCompanyLading, ConfirmOtherDriverPayment, OtherDriverPaymentByPositionView, LadingBillNumberListView, \
    SettleDriverImprests

router = DefaultRouter()
router.register('drivers', DriverModelView, basename='drivers')
router.register('cars', CarModelView, basename='cars')
router.register('drivings', DrivingModelView, basename='drivings')
router.register('associations', AssociationModelView, basename='associations')
router.register('ladingBillSeries', LadingBillSeriesModelView, basename='ladingBillSeries')

router.register('remittances', RemittanceModelView, basename='remittances')
router.register('ladings', LadingModelView, basename='ladings')
router.register('oilCompanyLadings', OilCompanyLadingModelView, basename='oilCompanyLadings')
router.register('otherDriverPayments', OtherDriverPaymentModelView, basename='otherDriverPayments')

urlpatterns = router.urls

urlpatterns += [
    url(r'^ladingBillSeries/byPosition$', LadingBillSeriesByPositionView.as_view()),

    url(r'^ladingBillNumbers/revoke$', RevokeLadingBillNumberView.as_view()),

    url(r'^remittances/byPosition$', RemittanceByPositionView.as_view()),
    url(r'^remittances/byCode$', RemittanceByCodeView.as_view()),

    url(r'^ladings/byPosition$', LadingByPositionView.as_view()),

    url(r'^oilCompanyLadings/byPosition$', OilCompanyLadingByPositionView.as_view()),

    url(r'^otherDriverPayments/byPosition$', OtherDriverPaymentByPositionView.as_view()),

    url(r'^settleDriverImprests$', SettleDriverImprests.as_view()),

    url(r'^remittances/(?P<pk>[0-9]+)/confirm/$', ConfirmRemittance.as_view(), name=''),
    url(r'^ladings/(?P<pk>[0-9]+)/confirm/$', ConfirmLading.as_view(), name=''),
    url(r'^oilCompanyLadings/(?P<pk>[0-9]+)/confirm/$', ConfirmOilCompanyLading.as_view(), name=''),
    url(r'^otherDriverPayments/(?P<pk>[0-9]+)/confirm/$', ConfirmOtherDriverPayment.as_view(), name=''),

    url(r'^export/otherDriverPayments/(?P<export_type>\S+)$', OtherDriverPaymentFormExportView.as_view(), name=''),
    url(r'^export/oilCompanyLadings/(?P<export_type>\S+)$', OilCompanyLadingFormExportView.as_view(), name=''),

    url(r'^report/otherDriverPayments$', OtherDriverPaymentReport.as_view(), name=''),
    url(r'^report/remittances/$', RemittanceListView.as_view()),
    url(r'^report/ladingBillSeriesList/$', LadingBillSeriesListView.as_view()),
    url(r'^report/ladings/$', LadingListView.as_view()),
    url(r'^report/oilCompanyLadings/$', OilCompanyLadingListView.as_view()),
    url(r'^report/oilCompanyLadingItems/$', OilCompanyLadingItemListView.as_view()),
    url(r'^report/ladingBillNumbers$', LadingBillNumberListView.as_view()),

    url(r'^report/ladings/(?P<export_type>\S+)', LadingListExportView.as_view(), name=''),
    url(r'^report/otherDriverPayments/(?P<export_type>\S+)', OtherDriverPaymentListExportView.as_view()),
    url(r'^report/ladingBillSeriesList/(?P<export_type>\S+)', LadingBillSeriesListExportView.as_view()),
    url(r'^report/ladingBillNumbers/(?P<export_type>\S+)', LadingBillNumberListExportView.as_view()),
    url(r'^report/remittances/(?P<export_type>\S+)', RemittanceListExportView.as_view()),
    url(r'^report/oilCompanyLadings/(?P<export_type>\S+)', OilCompanyLadingListExportView.as_view()),
    url(r'^report/oilCompanyLadingItems/(?P<export_type>\S+)', OilCompanyLadingItemListExportView.as_view()),

]
