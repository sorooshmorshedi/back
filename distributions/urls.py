from rest_framework.routers import DefaultRouter

from distributions.views import CommissionRangeModelView, VisitorModelView, PathModelView

router = DefaultRouter()
router.register('commissionRanges', CommissionRangeModelView, base_name='commission-range')
router.register('visitors', VisitorModelView, base_name='visitor')
router.register('paths', PathModelView, base_name='path')

urlpatterns = router.urls

urlpatterns += []
