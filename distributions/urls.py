from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from distributions.reports.lists import DistributionListView, DistributionListExportView, DistributionRemittanceView
from distributions.views import CommissionRangeModelView, VisitorModelView, PathModelView, DriverModelView, \
    DistributorModelView, CarModelView, DistributionModelView, GetDistributionByPositionView

router = DefaultRouter()
router.register('commissionRanges', CommissionRangeModelView, basename='commission-range')
router.register('visitors', VisitorModelView, basename='visitor')
router.register('paths', PathModelView, basename='path')
router.register('drivers', DriverModelView, basename='driver')
router.register('distributors', DistributorModelView, basename='distributor')
router.register('cars', CarModelView, basename='car')
router.register('distributions', DistributionModelView, basename='distribution')

urlpatterns = router.urls

urlpatterns += [
    url(r'^distributions/byPosition$', GetDistributionByPositionView.as_view(), name=''),
    url(r'^distributions/(?P<pk>[0-9]+)', DistributionRemittanceView.as_view(), name=''),

    url(r'^lists/distributions$', DistributionListView.as_view(), name=''),
    url(r'^lists/distributions/(?P<export_type>\S+)', DistributionListExportView.as_view(), name=''),

]
