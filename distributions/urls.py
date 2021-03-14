from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from distributions.reports.lists import DistributionListView, DistributionListExportView
from distributions.views import CommissionRangeModelView, VisitorModelView, PathModelView, DriverModelView, \
    DistributorModelView, CarModelView, DistributionModelView, GetDistributionByPositionView

router = DefaultRouter()
router.register('commissionRanges', CommissionRangeModelView, base_name='commission-range')
router.register('visitors', VisitorModelView, base_name='visitor')
router.register('paths', PathModelView, base_name='path')
router.register('drivers', DriverModelView, base_name='driver')
router.register('distributors', DistributorModelView, base_name='distributor')
router.register('cars', CarModelView, base_name='car')
router.register('distributions', DistributionModelView, base_name='distribution')

urlpatterns = router.urls

urlpatterns += [
    url(r'^distributions/byPosition$', GetDistributionByPositionView.as_view(), name=''),

    url(r'^lists/distributions$', DistributionListView.as_view(), name=''),
    url(r'^lists/distributions/(?P<export_type>\S+)', DistributionListExportView.as_view(), name=''),
]