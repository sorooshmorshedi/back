from rest_framework.routers import DefaultRouter

from distributions.views import CommissionRangeModelView, VisitorModelView

router = DefaultRouter()
router.register('commissionRanges', CommissionRangeModelView, base_name='commission-range')
router.register('visitors', VisitorModelView, base_name='visitor')

urlpatterns = router.urls

urlpatterns += []
