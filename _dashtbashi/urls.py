from rest_framework.routers import DefaultRouter

from _dashtbashi.views import DriverModelView, CarModelView, DrivingModelView

router = DefaultRouter()
router.register('drivers', DriverModelView, base_name='drivers')
router.register('cars', CarModelView, base_name='cars')
router.register('drivings', DrivingModelView, base_name='drivings')

urlpatterns = router.urls
