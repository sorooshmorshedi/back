from rest_framework.routers import DefaultRouter
from sobhan_admin.views import AdminUsersView

router = DefaultRouter()
router.register('users', AdminUsersView, base_name='admin-users')

urlpatterns = []

urlpatterns += router.urls
